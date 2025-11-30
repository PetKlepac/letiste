from django.urls import path
from ..views.invoices import invoices

urlpatterns = [
    path('', invoices, name='invoices'),
]