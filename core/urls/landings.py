from django.urls import path
from ..views.landings import landings

urlpatterns = [
    path('', landings, name='landings'),
]