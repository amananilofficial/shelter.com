from django.urls import path
from . import views

urlpatterns = [
    path('', views.agent_list, name='agents_list'),
    path('<int:agent_id>/', views.agent_detail, name='agent_detail'),
    path('contact/', views.agentcontact, name='agentcontact'),
    path('property-contact/', views.agent_property_contact, name='agent_property_contact'),
]