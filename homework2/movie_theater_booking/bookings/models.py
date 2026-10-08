from django.db import IntegrityError, models, transaction
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

class SeatAlreadyBooked(Exception):
    """Raised by Seat.book() when the seat is taken (spec 002 AC-3)."""


class Seat(models.Model):
    """One seat for one movie, so availability is per movie (spec 002 Open Q)."""

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=4)
    booking_status = models.BooleanField(default=False)

    class Meta:
        # Alphabetical, so A10 would sort before A2; fine for A1-A9 (plan §6).
        ordering = ["seat_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["movie", "seat_number"], name="unique_seat_number_per_movie"
            )
        ]

    def __str__(self):
        return f"{self.movie.title} {self.seat_number}"

    def book(self, user):
        """Book this seat for ``user`` and return the Booking.

        The one shared booking operation: the seat page, /api/seats/ and /api/bookings/
        all call this, so the rules live in one place (spec 002 AC-6).
        """
        taken = SeatAlreadyBooked(f"Seat {self.seat_number} is already booked")
        # Booking and status are saved together or not at all, so they can't disagree.
        with transaction.atomic():
            # Ask the database, not this instance, which may be stale. This gives the
            # friendly error, but two requests can both pass it before either saves...
            if Seat.objects.filter(pk=self.pk, booking_status=True).exists():
                raise taken
            try:
                booking = Booking.objects.create(movie=self.movie, seat=self, user=user)
            except IntegrityError:
                # ...so the one-to-one seat column is the real guard (AC-4). The loser gets
                # the same answer as AC-3, and leaving atomic() rolls back its writes.
                raise taken
            self.booking_status = True
            self.save(update_fields=["booking_status"])
        return booking

class Booking(models.Model):
    """A user's reservation of one seat. The user is always the signed-in user (spec 002 AC-5)."""

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # One-to-one: the database refuses a second booking of a seat, even in a race (AC-4).
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_date = models.DateField("booking date", auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.seat}"

