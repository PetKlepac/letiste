import os
import re
from datetime import datetime
from django.core.files import File
from django.core.management.base import BaseCommand
from ...models import Record
from django.utils.timezone import make_aware

FILENAME_RE = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{1,2}(?:\.\d+)?)\.wav$"
)

class Command(BaseCommand):
    help = "Load audio records from folder"

    def add_arguments(self, parser):
        parser.add_argument("folder", type=str)

    def handle(self, *args, **options):
        folder = options["folder"]

        for filename in os.listdir(folder):
            match = FILENAME_RE.match(filename)
            if not match:
                self.stdout.write(f"Skipping invalid filename: {filename}")
                continue

            year, month, day, hour, minute, second = match.groups()

            # Sekundy môžu mať desatiny, preto float
            second_float = float(second)
            sec_int = int(second_float)
            micro = int((second_float - sec_int) * 1_000_000)

            dt = datetime(
                int(year), int(month), int(day),
                int(hour), int(minute), sec_int, micro
            )

            # Urobiť datetime aware podľa nastavení Django
            dt = make_aware(dt)

            full_path = os.path.join(folder, filename)

            with open(full_path, "rb") as f:
                record = Record.objects.create(
                    date_time=dt,
                    audio_file=File(f, name=filename),
                    detection_probability=None
                )

            self.stdout.write(f"Loaded: {filename}")
