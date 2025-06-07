from django.urls import path
from . import views

app_name = 'team'

urlpatterns = [
    path('', views.team, name='team'),
    path('<int:team_id>', views.team_detail, name='team_detail'),
    path('<int:team_id>/contact/', views.team_contact, name='team_contact'),
]