from django.urls import include, path
from rest_framework import routers

from .views import FlightView, ReservationView

router = routers.DefaultRouter()
router.register('flights', FlightView)
router.register('reservations', ReservationView)

urlpatterns = [
    # ?-----------View Set (1'inci method)------------
    # path("", include(router.urls)),
    # ?-----------------------------------------------
]

# ?-----------View Set (2'nci method)------------
urlpatterns += router.urls
# ?-----------------------------------------------
