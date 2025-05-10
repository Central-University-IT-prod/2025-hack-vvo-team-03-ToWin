from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('comp/<int:comp_id>/', views.comp, name='comp'),
    path('join/<int:comp_id>/', views.join, name='join'),
    path('leave/<int:comp_id>/', views.leave, name='leave'),
    path('mygames/', views.mygames, name='mygames'),
    path('result/<int:comp_id>/', views.select_winners, name='result'),
    path('edit_game/<int:game_id>/<int:count1>/<int:count2>/', views.edit_game, name='edit_game'),
    path('api/', views.apimethod),
    path('api/competitions/', views.CompetitionListCreateAPIView.as_view(), name='competition-list-create'),
]
