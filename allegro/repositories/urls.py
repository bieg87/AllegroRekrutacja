from django.urls import path
from .views import ListRepositoriesView, SumOfStarsView, UserLanguagesView

urlpatterns = [
    path('repositories/<str:user>/', ListRepositoriesView.as_view()),
    path('repositories/<str:user>/sum', SumOfStarsView.as_view()),
    path('repositories/<str:user>/languages', UserLanguagesView.as_view()),
    ]
