from django.urls import path
from ..views.customers import (
    customers,
    add_customer,
    edit_customer,
    update_customer,
    delete_customer,
    customer_detail,

    add_aircraft,        # NEW
    edit_aircraft,       # NEW
    delete_aircraft,     # NEW
)

urlpatterns = [
    path('', customers, name='customers'),
    path('add/', add_customer, name='add_customer'),
    path('<int:pk>/detail/', customer_detail, name='customer_detail'),

    # 🔹 NEW aircraft routes
    path('<int:customer_id>/aircraft/add/', add_aircraft, name='add_aircraft'),
    path('aircraft/edit/', edit_aircraft, name='edit_aircraft'),
    path('aircraft/delete/', delete_aircraft, name='delete_aircraft'),

    path('<int:pk>/edit/', edit_customer, name='edit_customer'),
    path('update/', update_customer, name='update_customer'),
    path('delete/', delete_customer, name='delete_customer'),
]
