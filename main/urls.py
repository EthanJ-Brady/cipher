from django.urls import path

from . import views

urlpatterns = [
    path('gameboard/', views.gameboard, name='gameboard'),
    path('getcardtitles/', views.get_card_titles, name='getCardTitles'),
    path('', views.index, name='index')
]