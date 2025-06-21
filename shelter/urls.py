from django.urls import path
from . import views
from agents.views import agent_property_contact

urlpatterns = [
    path('',views.index,name='index'),
    path('property-detail/<slug:slug>',views.propertyDetail,name='property_detail'),
    path('properties-list/',views.propertiesList,name='properties_list'),
    path('contact/',views.contact,name='contact'),
    path('search/',views.searchResult,name='search'),
    path('services/',views.Services,name='services'),
    path('about/', views.about_view, name='about'),
    path('quick-contact/',views.Quick_Contact,name='quickcontact'),
    path('contact-agent/',views.UserAgentContact,name='agentcontact'),
    path('property-agent-contact/', agent_property_contact, name='agent_property_contact'),
    path('newsletter/signup/', views.newsletter_signup, name='newsletter_signup'),
    path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('cookies/', views.cookies_view, name='cookies'),
    path('sale/', views.sale_view, name='sale_view'),
    path('rent/', views.rent_view, name='rent_view'),
    path('property-management/', views.property_management_view, name='property_management_view'),
    path('buy/', views.buy_view, name='buy_view')
]