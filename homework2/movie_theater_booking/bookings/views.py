from django.shortcuts import render
from rest_framework import viewsets

from .models import Movie
from .serializers import MovieSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """CRUD for movies at /api/movies/ (spec 001). Ordering comes from Movie.Meta."""

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


def movie_list(request):
    """The movie list page; reads the same Movie data as the API (spec 001)."""
    return render(request, "bookings/movie_list.html", {"movies": Movie.objects.all()})
