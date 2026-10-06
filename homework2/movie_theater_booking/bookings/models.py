from django.db import models
from django.conf import settings
# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    release_date = models.DateField("release date")
    duration = models.PositiveIntegerField()

class Seat(models.Model):
    seat_number = models.PositiveIntegerField()
    booking_status = models.BooleanField(default=False)

class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_date = models.DateField("booking date")

