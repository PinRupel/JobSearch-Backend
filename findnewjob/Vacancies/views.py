from django.shortcuts import render

from rest_framework import generics

from .models import Vacancy
from Vacancies.serializers import VacancySerializer


class VacancyAPIView(generics.ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer


class VacancyListCreateView(generics.ListCreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
