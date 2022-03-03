from datetime import date, datetime

from django.shortcuts import render
from rest_framework import viewsets

from .models import Flight, Reservation
from .permissions import IsStuffOrReadOnly
from .serializers import (FlightSerializer, ReservationSerializer,
                          StaffFlightSerializer)


class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    # ! Tuple kullandığımız için sonunda virgül koymak önemli
    permission_classes = (IsStuffOrReadOnly,)

    #! staff userlar için farklı serializer
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return StaffFlightSerializer
        return super().get_serializer_class()

    #! normal bir kullanıcı geçmiş flightları görmesini istemiyoruz.
    def get_queryset(self):
        now = datetime.now()
        # ! formatımız nasılsa ona uyduruyoruz.
        current_time = now.strftime("%H:%M:%S")
        print("current_time: ", current_time)
        today = date.today()
        print("Today: ", today)
        if self.request.user.is_staff:
            return super().get_queryset()
        else:
            #! önce bugünden büyükleri alıyoruz. daha sonra aynı gün now'dan büyük saatleri alıyoruz. daha sonra iki queryset'i birleştiriyoruz.
            queryset = Flight.objects.filter(dateOfDeparture__gt=today)
            if Flight.objects.filter(dateOfDeparture=today):
                today_queryset = Flight.objects.filter(dateOfDeparture=today).filter(
                    estimatedTimeOfDeparture__gt=current_time)
                # ! union ile birden fazla queryseti birleştiriyoruz.
                queryset = queryset.union(today_queryset)
            return queryset


class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    #! user sadece kendi reservationlarını görsün, admin hepsini görsün. (get_queryset --> genericAPIView içerisinde)
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)
