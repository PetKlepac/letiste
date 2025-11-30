from django.urls import path
from ..views.records import records

urlpatterns = [
    path('', records, name='records'),
]