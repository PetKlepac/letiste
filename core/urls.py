from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recordings/', views.recordings, name='recordings'),
    path('landings/', views.landings, name='landings'),
    path('customers/', views.customers, name='customers'),
    path('aircraft/', views.aircraft, name='aircraft'),
    path('invoices/', views.invoices, name='invoices'),
]
