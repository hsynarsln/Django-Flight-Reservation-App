from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from .serializers import RegisterSerializer


# Create your views here.
class RegisterAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
