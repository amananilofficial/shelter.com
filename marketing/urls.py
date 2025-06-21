# filepath: d:\completed\shelter.com\marketing\urls.py
from django.urls import path
from . import views

app_name = 'marketing'

urlpatterns = [
    path('', views.marketing_dashboard, name='dashboard'),
    path('properties/', views.property_list, name='property_list'),
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('campaigns/create/', views.create_campaign, name='create_campaign'),
    path('leads/', views.lead_list, name='lead_list'),
]