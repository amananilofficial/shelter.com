# filepath: d:\completed\shelter.com\crm\urls.py
from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    path('', views.crm_dashboard, name='dashboard'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('customers/add/', views.add_customer, name='add_customer'),
    path('customers/<int:customer_id>/edit/', views.edit_customer, name='edit_customer'),
    path('customers/<int:customer_id>/history/', views.customer_history, name='customer_history'),
    path('customers/upload/', views.upload_customers, name='upload_customers'),
    path('customers/<int:customer_id>/interaction/', views.add_interaction, name='add_interaction'),
    path('transfers/', views.transfer_list, name='transfer_list'),
    path('transfers/create/', views.create_transfer, name='create_transfer'),
    path('transfers/<int:transfer_id>/', views.transfer_detail, name='transfer_detail'),
]