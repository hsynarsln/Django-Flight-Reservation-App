from django.contrib.auth.models import User
from django.db import models


#! Field tanımlarken max_length=25 --> dediğimizde o kadarlık alan ayırıyor. Bu değerleri en optimum şekilde kullanmamız gerekir.
class Flight(models.Model):
    flightNumber = models.CharField(max_length=10)
    operatingAirlines = models.CharField(max_length=25)
    departureCity = models.CharField(max_length=30)
    arrivalCity = models.CharField(max_length=30)
    # ! manuel olarak girileceği için içini boş bırakıyoruz
    dateOfDeparture = models.DateField()
    estimatedTimeOfDeparture = models.TimeField()

    def __str__(self):
        return f'{self.flightNumber} - {self.departureCity} - {self.arrivalCity}'


class Passenger(models.Model):
    firstName = models.CharField(max_length=40)
    lastName = models.CharField(max_length=40)
    email = models.EmailField(max_length=100)
    phoneNumber = models.IntegerField()
    updatedDate = models.DateTimeField(auto_now=True)
    createdDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.firstName} {self.lastName}'


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    passenger = models.ManyToManyField(Passenger, related_name='passenger')
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name='reservations')

    def __str__(self):
        return f'{self.user} - {self.passenger} - {self.flight}'
