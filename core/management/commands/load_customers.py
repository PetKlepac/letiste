# ---------------------------------------------------------------
# USAGE:
#   python manage.py load_customers 20
#
# This creates user1 ... user20 with:
#   username = user1
#   email    = user1@user.com
#   password = user1
#
# A CSV with all created credentials is saved to:
#   MEDIA_ROOT/created_customers/customers_<timestamp>.csv
# ---------------------------------------------------------------

import os
import csv
from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from ...models import Customer

User = get_user_model()


class Command(BaseCommand):
    help = "Create N dummy customers (user1, user2 ...) and save credentials to MEDIA_ROOT."

    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            type=int,
            help="How many customers to create"
        )

    def handle(self, *args, **options):
        count = options["count"]

        # Prepare output directory
        out_dir = os.path.join(settings.MEDIA_ROOT, "created_customers")
        os.makedirs(out_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_file = os.path.join(out_dir, f"customers_{timestamp}.csv")

        created_entries = []

        for i in range(1, count + 1):
            username = f"user{i}"
            email = f"user{i}@user.com"
            password = username
            company_name = f"Company {username}"
            vat_id = f"VAT123{username}"

            # Create the user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Create corresponding Customer
            Customer.objects.create(
                user=user,
                company_name=company_name,
                vat_id=vat_id
            )

            created_entries.append([
                username, email, password, company_name, vat_id
            ])

            self.stdout.write(self.style.SUCCESS(f"Created customer {username}"))

        # Save output CSV
        with open(out_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "email", "password", "company_name", "vat_id"])
            writer.writerows(created_entries)

        self.stdout.write(self.style.SUCCESS(
            f"\nSaved credentials to: {out_file}\n"
        ))
