from django.urls import path
from . import views

app_name = 'team'

urlpatterns = [
    path('', views.team, name='team'),
    path('<int:team_id>', views.team_detail, name='team_detail'),
    path('<int:team_id>/contact/', views.team_contact, name='team_contact'),
    path('api/role/', views.check_user_role, name='check_role'),
    path('api/export/', views.export_team_data, name='export_data'),
    path('api/sync/', views.sync_with_apps, name='sync_apps'),
]