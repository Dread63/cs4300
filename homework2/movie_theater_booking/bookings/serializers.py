from rest_framework import serializers
from .models import Movie, Seat, Booking

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "description", "release_date", "duration"]

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["id", "movie", "seat_number", "booking_status"]

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "movie", "seat", "user", "booking_date"]
        # Set by Seat.book(), never by the client (spec 002 AC-5).
        read_only_fields = ["movie", "user", "booking_date"]
