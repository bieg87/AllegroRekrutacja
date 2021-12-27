# AllegroRekrutacja
Projekt na potrzeby rekrutacji do Allegro

Instrukcja uruchomienia

Projekt został stworzony na systemie operacyjnym Windows 10 i na nim powinien zostać uruchomiony
Wykorzystano framework Django.

Na początku należy zainstalować program git i python 3.8.5

Następnie trzeba sklonować repozytorium:

git clone https://github.com/bieg87/AllegroRekrutacja.git

W dalszej kolejności należy wejść do AllegroRekrutacja i stworzyć wirtualne środowisko za pomocą programu venv:

python -m venv ./env

i uruchomić wirtualne środowisko:

env\Scripts\activate

Następnie należy zainstalować biblioteki:

pip install -r requirements.txt

W katalogu, w którym znajduje się plik manage.py należy wpisać polecenie:

python manage.py runserver

Serwer powinien wystartować.

UWAGI DO PROJEKTU 

Endpoints:

1. Listownie repozytorium danego użytkownika z liczbą gwaizdek:

GET http://127.0.0.1:8000/git-api/repositories/<nazwa użytkownika>

np. http://127.0.0.1:8000/git-api/repositories/allegro

2. Obliczanie sumy gwiazdek danego repozytorium

GET http://127.0.0.1:8000/git-api/repositories/<nazwa użytkownika>/sum

np. http://127.0.0.1:8000/git-api/repositories/allegro/sum

3. Listowanie języków wykorzystanych przez danego użytkownika wraz z rozmiarem w bajtach

GET http://127.0.0.1:8000/git-api/repositories/<nazwa użytkownika>/languages

W typ przypadku należy być ostrożnym z wyborem użytkownika, ponieważ dla nieautoryzowanego 
użytkownika maksymalna liczba zapytań wysłana w ciągu godziny do GitHub API wynosi 60.
Zapytania o języki programowania wysyłane są do każdego repozytorium oddzielnie. Zatem jeśli dany
użytkownik będzie miał więcej niż 60 repozytoriów dostęp do GitHub API zablokuje się. 

np. http://127.0.0.1:8000/git-api/repositories/bieg87/languages

Program nie jest pokryty testami oraz nie zawiera interfejsu użytkownika, ponieważ nie było tego w wymaganiach zadania. 
W repozytorium na GitHub upublicznio klucz, co w warunkach produkcyjnych jest niedopuszczalne. Zrobiono to tylko w celu 
uproszczenia uruchomienia.