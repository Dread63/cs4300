from rest_framework import viewsets

from .models import Movie
from .serializers import MovieSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """CRUD for movies at /api/movies/ (spec 001). Ordering comes from Movie.Meta."""

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
