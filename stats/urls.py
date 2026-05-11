from django.urls import path
from . import views

app_name = 'stats'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('player/<int:player_id>/', views.player_detail, name='player_detail'),
    path('team/<int:team_id>/', views.team_detail, name='team_detail'),
    path('team/<int:team_id>/season/<str:season>/', views.team_season_games, name='team_season_games'),
    path('api/search/', views.search_api, name='search_api'),
]
