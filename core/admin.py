from django.contrib import admin
from .models import Customer, Aircraft, Record, Landing, Invoice

class AircraftInline(admin.TabularInline):
    model = Aircraft.customers.through     # ← this is the link table
    extra = 1                              # how many empty rows to show
    verbose_name = "Aircraft"
    verbose_name_plural = "Aircraft linked to this customer"

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "contact", "full_address")
    search_fields = ("name", "city", "country")

@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ("registration", "name", "get_customers")
    search_fields = ("registration", "name")
    filter_horizontal = ("customers",)

    def get_customers(self, obj):
        return ", ".join([c.name for c in obj.customers.all()])

    get_customers.short_description = "Customers"

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ("date_time", "validation_status", "validated_by")
    list_filter = ("validation_status",)
    search_fields = ("validated_by__username",)

@admin.register(Landing)
class LandingAdmin(admin.ModelAdmin):
    list_display = ("id", "date_time", "price", "aircraft", "invoice")
    list_filter = ("invoiced",)
    search_fields = ("aircraft__registration",)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "date_issued", "amount", "paid", "customer")
    list_filter = ("paid",)
    search_fields = ("customer__name",)
