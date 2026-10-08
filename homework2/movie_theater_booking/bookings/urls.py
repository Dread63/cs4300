from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# The router generates the list (/movies/) and detail (/movies/<id>/) routes for each viewset.
router = DefaultRouter()
router.register("movies", views.MovieViewSet)
router.register("seats", views.SeatViewSet, basename="seat")

urlpatterns = [
    path("", views.movie_list, name="movie_list"),
    path("movies/<int:movie_id>/seats/", views.seat_booking, name="book_seat"),
    path("api/", include(router.urls)),
]
