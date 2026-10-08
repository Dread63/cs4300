"""`python manage.py seed_demo`: demo movies, seats A1-A5, and an optional demo account.

Render's free tier rebuilds the SQLite database on every deploy, so build.sh runs this
each time. It's safe to run again: nothing is duplicated, and existing bookings stay.
"""
import os
from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from bookings.models import Movie, Seat

MOVIES = [
    ("Dune", "A noble family becomes embroiled in a war for the desert planet Arrakis.", date(2021, 10, 22), 155),
    ("Arrival", "A linguist works to communicate with alien visitors.", date(2016, 11, 11), 116),
    ("Up", "An old man ties thousands of balloons to his house and flies away.", date(2009, 5, 29), 96),
]
SEAT_NUMBERS = ["A1", "A2", "A3", "A4", "A5"]


class Command(BaseCommand):
    help = "Create demo movies with seats A1-A5, and a 'demo' user if DEMO_PASSWORD is set."

    def handle(self, *args, **options):
        for title, description, release_date, duration in MOVIES:
            movie, _ = Movie.objects.get_or_create(
                title=title,
                defaults={"description": description, "release_date": release_date, "duration": duration},
            )
            for number in SEAT_NUMBERS:
                Seat.objects.get_or_create(movie=movie, seat_number=number)

        # The password comes from the environment, never from code (AGENTS.md).
        password = os.environ.get("DEMO_PASSWORD")
        if password:
            demo, _ = User.objects.get_or_create(username="demo")
            demo.set_password(password)
            demo.save()
            self.stdout.write("Demo user 'demo' is ready.")
        else:
            self.stdout.write("DEMO_PASSWORD not set; no demo user created.")
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(MOVIES)} movies with seats {', '.join(SEAT_NUMBERS)}."))
