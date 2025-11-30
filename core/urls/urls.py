from django.urls import path, include

urlpatterns = [
    path('', include('core.urls.home')),
    path('customers/', include('core.urls.customers')),
    path('recordings/', include('core.urls.records')),
    path('landings/', include('core.urls.landings')),
    path('invoices/', include('core.urls.invoices')),
]
