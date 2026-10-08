from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
# Create your models here.

class Movie(models.Model):
    """A film that can be listed and booked. Duration is in whole minutes."""

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    release_date = models.DateField("release date")
    # PositiveIntegerField allows 0; a movie must run at least a minute (spec 001 AC-6).
    duration = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        # Newest first, so the page and the API agree without each sorting (AC-10).
        ordering = ["-release_date"]

    def __str__(self):
        return self.title

class Seat(models.Model):
    seat_number = models.PositiveIntegerField()
    booking_status = models.BooleanField(default=False)

class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_date = models.DateField("booking date")

