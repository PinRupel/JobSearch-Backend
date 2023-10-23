from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from Users.serializers import ApplicantRegisterSerializer, EmployerRegisterSerializer


class ApplicantRegisterApiView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ApplicantRegisterSerializer


class EmployerRegisterApiView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmployerRegisterSerializer
    



