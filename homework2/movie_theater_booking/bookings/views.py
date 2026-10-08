from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Booking, Movie, Seat, SeatAlreadyBooked
from .serializers import BookingSerializer, MovieSerializer, SeatSerializer


class SeatTaken(APIException):
    """409 Conflict for SeatAlreadyBooked: the request is fine, but the seat's state refuses it.

    Both booking endpoints raise this, so they answer a taken seat the same way (002 AC-3).
    """

    status_code = status.HTTP_409_CONFLICT


class MovieViewSet(viewsets.ModelViewSet):
    """CRUD for movies at /api/movies/ (spec 001). Ordering comes from Movie.Meta."""

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    """Seat availability at /api/seats/, optionally ?movie=<id> (spec 002 AC-10).

    Read-only: seats are created in the admin (spec 002 §6).
    """

    serializer_class = SeatSerializer

    def get_queryset(self):
        seats = Seat.objects.all()
        movie_id = self.request.query_params.get("movie")
        if movie_id:
            # The filter would crash (500) on a non-number, so refuse it as bad input (AC-14).
            if not movie_id.isdecimal():
                raise serializers.ValidationError({"movie": ["Must be a movie id (a whole number)."]})
            seats = seats.filter(movie_id=movie_id)
        return seats

    # Browsing seats is public; booking needs a signed-in user (AC-8).
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def book(self, request, pk=None):
        """POST /api/seats/<id>/book/: book this seat for the signed-in user (AC-11)."""
        # The user comes from the session, never from request data (AC-5).
        try:
            booking = self.get_object().book(request.user)
        except SeatAlreadyBooked as taken:
            raise SeatTaken(str(taken))
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class BookingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """The signed-in user's booking history at /api/bookings/ (spec 003)."""

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only ever my bookings: every list and detail lookup goes through here (AC-2, AC-3).
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """POST /api/bookings/ {"seat": id}: book through 002's Seat.book() (AC-7).

        Not serializer.save(): that would skip the booking rules and booking_status.
        """
        seat = serializer.validated_data["seat"]
        try:
            serializer.instance = seat.book(self.request.user)
        except SeatAlreadyBooked as taken:
            raise SeatTaken(str(taken))


def movie_list(request):
    """The movie list page; reads the same Movie data as the API (spec 001)."""
    return render(request, "bookings/movie_list.html", {"movies": Movie.objects.all()})


def seat_booking(request, movie_id):
    """The seat booking page for one movie: see which seats are free, and book one (spec 002)."""
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == "POST":
        # Viewing is public; booking needs a signed-in user, then back to this page (AC-8).
        if not request.user.is_authenticated:
            return redirect_to_login(request.path)
        seat_id = request.POST.get("seat", "")
        if not seat_id.isdecimal():  # junk would crash the lookup (500); it's no such seat
            raise Http404("No such seat")
        # Looking up through movie.seats means another movie's seat id is also a 404.
        seat = get_object_or_404(movie.seats, pk=seat_id)
        try:
            seat.book(request.user)
        except SeatAlreadyBooked as taken:
            messages.error(request, str(taken))  # AC-3: same message as the API's 409
        else:
            messages.success(request, f"Seat {seat.seat_number} booked for {movie.title}")
        # Redirect after POST, so refreshing the page doesn't resubmit the booking (AC-2).
        return redirect("book_seat", movie_id=movie.id)
    return render(
        request, "bookings/seat_booking.html", {"movie": movie, "seats": movie.seats.all()}
    )


# Signed out: to the sign-in page, then back here (AC-6).
@login_required
def booking_history(request):
    """My Bookings: the signed-in user's bookings, newest first (spec 003)."""
    # Only mine (AC-2); select_related loads movie and seat in the same query.
    bookings = Booking.objects.filter(user=request.user).select_related("movie", "seat")
    return render(request, "bookings/booking_history.html", {"bookings": bookings})
