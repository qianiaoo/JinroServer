from django.urls import path
from . import views

urlpatterns = [
    path('hall/', views.hall_list),
    path('join/', views.join_game),
    path('start/', views.game_start),
]