from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import RegisterSerializer


# Create your views here.
class RegisterAPI(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    #! aşağıdaki fonksiyoun ile user kaydedince response olarak message döndürüyoruz.
    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        #!-----------Token key ekleme--------------
        token = Token.objects.create(user=user)
        data = serializer.data
        data['token'] = token.key
        headers = self.get_success_headers(serializer.data)
        #!----------------------------------------
        #! token oluşturduktan sonra headers ile göndermemiz gerekiyor
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
