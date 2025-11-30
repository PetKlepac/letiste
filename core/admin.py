from django.contrib import admin
from .models import User, Customer, Aircraft, Record, Landing, Invoice


# ------------------------
# USER
# ------------------------

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "phone_number", "city", "country")
    search_fields = ("username", "email", "city", "country")


# ------------------------
# CUSTOMER
# ------------------------

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name", "vat_id")
    search_fields = ("user__username", "company_name", "vat_id")


# ------------------------
# AIRCRAFT
# ------------------------

@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ("registration", "name", "owner")  # removed assigned_by
    search_fields = ("registration", "name")
    list_filter = ("owner",)


# ------------------------
# RECORD
# ------------------------

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("date_time", "detection_probability", "validation_status")  # removed validated_by
    list_filter = ("validation_status",)
    search_fields = ("audio_file",)  # validated_by no longer exists


# ------------------------
# LANDING
# ------------------------

@admin.register(Landing)
class LandingAdmin(admin.ModelAdmin):
    list_display = ("id", "date_time", "price", "aircraft", "invoice")
    list_filter = ("invoiced", "date_time")
    search_fields = ("aircraft__registration",)


# ------------------------
# INVOICE
# ------------------------

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "date_issued", "amount", "paid", "customer")
    search_fields = ("customer__user__username",)
    list_filter = ("paid", "date_issued")
