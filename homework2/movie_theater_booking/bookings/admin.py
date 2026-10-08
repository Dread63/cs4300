from django.contrib import admin

from .models import Booking, Movie, Seat

# Staff create movies, seats and user accounts here (spec 002 Open Q).
admin.site.register([Movie, Seat, Booking])
