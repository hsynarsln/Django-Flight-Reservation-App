from django.urls import include, path

from .views import RegisterAPI

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path("auth/register/", RegisterAPI.as_view(), name="register"),
]
