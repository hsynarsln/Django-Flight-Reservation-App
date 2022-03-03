from rest_framework import serializers

from .models import Flight, Passenger, Reservation


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            'id',
            'flightNumber',
            'operatingAirlines',
            'departureCity',
            'arrivalCity',
            'dateOfDeparture',
            'estimatedTimeOfDeparture'
        )
