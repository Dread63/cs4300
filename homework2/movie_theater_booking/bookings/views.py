from django.shortcuts import render
from .models import Movie, Seat, Booking
from rest_framework import permissions, viewsets
# Create your views here.

class MovieViewSet(viewsets.ModelViewSet)

