from django.urls import path
from ..views.landings import landings, add_landing, landing_detail

urlpatterns = [
    path("", landings, name="landings"),  # /landings/
    path("add/", add_landing, name="add_landing"),  # /landings/add/
    path("<int:pk>/", landing_detail, name="landing_detail"),  # /landings/5/
]
