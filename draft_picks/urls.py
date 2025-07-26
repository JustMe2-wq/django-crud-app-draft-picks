from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('teams/', views.team_index, name='team_index'),
    path('teams/<int:team_id>/', views.team_detail, name='team_detail'),
    path('teams/create/', views.TeamCreate.as_view(), name='team_create'),
    path('teams/<int:pk>/update/', views.TeamUpdate.as_view(), name='team_update'),
    path('teams/<int:pk>/delete/', views.TeamDelete.as_view(), name='team_delete'),
    path('teams/<int:team_id>/add-draft/', views.add_draft, name='add_draft'),
    path('draft/<int:pk>/delete/', views.DraftDelete.as_view(), name='draft_delete'),
    path('players/create/', views.PlayerCreate.as_view(), name='player_create'),
    path('players/<int:pk>/', views.PlayerDetail.as_view(), name='player_detail'),
    path('players/', views.PlayerList.as_view(), name='player_index'),
    path('players/<int:pk>/update/', views.PlayerUpdate.as_view(), name='player_update'),
    path('players/<int:pk>/delete/', views.PlayerDelete.as_view(), name='player_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]