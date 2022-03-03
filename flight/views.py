from django.shortcuts import render
from rest_framework import viewsets

from .models import Flight, Reservation
from .serializers import FlightSerializer


class FlightView(viewsets.ModelViewSet):
    pass
