from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("manager", "Letecký správce"),
        ("customer", "Zákazník"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")
    phone_number = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def full_address(self):
        parts = [self.street, self.city, self.postal_code, self.country]
        return ", ".join([p for p in parts if p])



class Aircraft(models.Model):
    registration = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_aircraft"
    )
    customers = models.ManyToManyField(
        User,
        blank=True,
        related_name='aircraft'
    )

    def __str__(self):
        return f"{self.registration} ({self.name})"

class Invoice(models.Model):
    date_issued = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    paid = models.BooleanField(default=False)
    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invoices"
    )
    sent_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_invoices"
    )

    def __str__(self):
        return f"Invoice #{self.id} - {self.customer or 'No customer'}"


class Record(models.Model):
    date_time = models.DateTimeField()
    audio_file = models.FileField(upload_to="records/")
    detection_probability = models.FloatField(null=True, blank=True)
    validation_status = models.BooleanField(default=False)
    validated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="validated_records"
    )

    def __str__(self):
        return f"Record {self.date_time}"


class Landing(models.Model):
    record = models.ForeignKey(
        Record,
        on_delete=models.SET_NULL,
        related_name="landings",
        null=True,
        blank=True
    )
    date_time = models.DateTimeField()
    price = models.IntegerField(default=0)
    aircraft = models.ForeignKey(
        Aircraft,
        on_delete=models.SET_NULL,
        related_name="landings",
        null=True,
        blank=True
    )
    invoiced = models.BooleanField(default=False)
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="landings"
    )
    invoiced_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="invoiced_landings")

    def __str__(self):
        return f"Landing #{self.id}"
