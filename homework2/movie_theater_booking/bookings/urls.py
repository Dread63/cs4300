from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# The router generates the list (/movies/) and detail (/movies/<id>/) routes for each viewset.
router = DefaultRouter()
router.register("movies", views.MovieViewSet)

urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("api/", include(router.urls)),
]
