"""Load the Newton voter CSV into the database.

Usage: python manage.py load_voters [path/to/newton_voters.csv]

Same parsing rules as models.load_data(), but uses bulk_create so the
~59k rows load in seconds instead of minutes.
"""

import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from voter_analytics.models import Voter


def parse_bool(value):
    return value.strip().upper() == "TRUE"


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()


class Command(BaseCommand):
    help = "Replace all voters with the rows in newton_voters.csv"

    def add_arguments(self, parser):
        parser.add_argument("path", nargs="?", default="data/newton_voters.csv")

    def handle(self, *args, path, **options):
        voters, skipped = [], 0
        with open(path, newline="") as f:
            for row in csv.DictReader(f):
                try:
                    apt = row["Residential Address - Apartment Number"].strip()
                    voters.append(Voter(
                        first_name=row["First Name"].strip(),
                        last_name=row["Last Name"].strip(),
                        street_number=row["Residential Address - Street Number"].strip(),
                        street_name=row["Residential Address - Street Name"].strip(),
                        apartment_number=apt or None,
                        zip_code=row["Residential Address - Zip Code"].strip(),
                        date_of_birth=parse_date(row["Date of Birth"]),
                        date_of_registration=parse_date(row["Date of Registration"]),
                        party_affiliation=row["Party Affiliation"],
                        precinct_number=row["Precinct Number"].strip(),
                        v20state=parse_bool(row["v20state"]),
                        v21town=parse_bool(row["v21town"]),
                        v21primary=parse_bool(row["v21primary"]),
                        v22general=parse_bool(row["v22general"]),
                        v23town=parse_bool(row["v23town"]),
                        voter_score=int(row["voter_score"]),
                    ))
                except (KeyError, ValueError):
                    skipped += 1

        with transaction.atomic():
            Voter.objects.all().delete()
            Voter.objects.bulk_create(voters, batch_size=2000)

        self.stdout.write(self.style.SUCCESS(
            f"Loaded {len(voters)} voters ({skipped} rows skipped)."
        ))
