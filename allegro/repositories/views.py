import collections
import functools
import json
import operator

from rest_framework import status
import requests
from rest_framework.response import Response
from rest_framework.views import APIView


class ListRepositoriesView(APIView):
    """
    Klasa do wystawienia API z jedną metodą get, która przekazuje repozytoria danego użytkownika z liczbą gwiazdek
    """
    def get(self, request, user):
        """
        Metoda wysyła odpowiedź na żądanie get
        :param request: żądanie
        :param user: wyszukiwany użytkownik
        :return: zwracana odpowiedź z wylistowanymi repozytoriami z liczbą gwiazdek
        """
        response = get_user_repositories(user)
        repositories = self.get_repository_names_and_stars(response)

        if not repositories:
            return Response([], status=status.HTTP_404_NOT_FOUND)

        return Response(json.dumps(repositories), status=status.HTTP_200_OK)

    def get_repository_names_and_stars(self, response):
        """
        Metoda przekszatłca odpowiedź z GitHub API do odpowiedniego formatu JSON
        :param response: odpwiedź z GitHub
        :return: JSON do przekazania użytkownikowi
        """
        repositories = []
        json_response = response.json()
        for repository in json_response:
            repositories.append({'name': repository['name'], 'stars': repository['stargazers_count']})

        return repositories


class SumOfStarsView(APIView):
    """
    Klasa wystawia API do obliczania sumy gwiazdek repozystoriów danego użytkownika
    """
    def get(self, request, user):
        """
        Metoda wysyła odpowiedź na żądanie get
        :param request: żądanie
        :param user: nazwa użytkownika
        :return: zwraca sumę gwiazdek repozytoriów danego użytkownika
        """
        response = get_user_repositories(user)
        sum_of_stars = self.sum_repositories_stars(response)

        if sum_of_stars is None:
            return Response([], status=status.HTTP_404_NOT_FOUND)

        return Response(json.dumps({'sum_of_stars': sum_of_stars}), status=status.HTTP_200_OK)

    def sum_repositories_stars(self, response):
        """
        Metoda pobiera liczby gwiazdek repozytoriów, zapisuje w liście i sumuje
        :param response: odpowiedź z GitHub
        :return: suma gwiazdek danego użytkownika
        """
        if response.status_code == status.HTTP_404_NOT_FOUND:
            return None

        repositories = []
        json_response = response.json()

        for repository in json_response:
            repositories.append(repository['stargazers_count'])

        return sum(repositories)


class UserLanguagesView(APIView):
    """
    Klasa wystawia API dla wyświatlania języków programowania wykorzystywanych przez użytkownika i liczby bajtów kodu
    """
    def get(self, request, user):
        """
        Metoda wysyła odpowiedź na żądanie get
        :param request: żądanie
        :param user: nazwa użytkownika
        :return: zwraca listę jęzków wraz z liczbą bajtów
        """
        response = get_user_repositories(user)
        repositories_names = self.get_all_repositories_names(response)

        if repositories_names is None:
            return Response([], status=status.HTTP_404_NOT_FOUND)

        languages = self.get_languages(repositories_names, user)
        languages_result = dict(sorted(languages.items(), key=lambda item: item[1], reverse=True))

        return Response(json.dumps(languages_result), status=status.HTTP_200_OK)

    def get_all_repositories_names(self, response):
        """
        Metoda pobiera nazwy wszystkich repozytoriów danego użytkownika
        :param response: JSON z GitHub
        :return: Lista nazw repozytoriów danego użytkownika
        """
        repositories_names = []
        if response.status_code == status.HTTP_404_NOT_FOUND:
            return None
        json_response = response.json()

        for repository in json_response:
            repositories_names.append(repository['name'])

        return repositories_names

    def get_languages(self, repository_names, user):
        """
        Metoda dodaje liczby bajtów wszystkich wykorzystywanych języków
        :param repository_names: nazwy repozytoriów
        :param user: nazwa użytkownika
        :return: słownik z nazwami języków i liczbą bajtów
        """
        languages = []
        for name in repository_names:
            languages.append(self.get_repository_languages(name, user))

        return dict(functools.reduce(operator.add, map(collections.Counter, languages)))

    def get_repository_languages(self, name, user):
        """
        Metoda pobiera z GitHub statystyki języków dla każdego repozytorium
        :param name: nazwa repozytorium
        :param user: nazwa użytkownika
        :return: JSON z GitHub API
        """
        response = requests.get('https://api.github.com/repos/' + user + '/' + name + '/languages')

        return response.json()


def get_user_repositories(user):
    """
    Funkcja wysyła żądanie get do GitHub API
    :param user: wyszukiwany użytkownik
    :return: zwracana odpowiedź z GitHub API
    """
    response = requests.get('https://api.github.com/users/' + user + '/repos')

    return response
