from django.shortcuts import render
from rest_framework import serializers, viewsets

from .models import Movie, Seat
from .serializers import MovieSerializer, SeatSerializer


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


def movie_list(request):
    """The movie list page; reads the same Movie data as the API (spec 001)."""
    return render(request, "bookings/movie_list.html", {"movies": Movie.objects.all()})
