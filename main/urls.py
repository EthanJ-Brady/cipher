from django.urls import path

from . import views

urlpatterns = [
    path('gameboard/', views.gameboard, name='gameboard'),
    path('', views.index, name='index')
]