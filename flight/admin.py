from django.contrib import admin

from .models import Flight, Passenger, Reservation

# Register your models here.
admin.site.register(Flight)
admin.site.register(Reservation)
admin.site.register(Passenger)
