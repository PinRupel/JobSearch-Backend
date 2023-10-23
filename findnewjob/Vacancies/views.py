from django.shortcuts import render

from rest_framework import generics

from .models import Vacancy
from Vacancies.serializers import VacancySerializer
from Users.permissions import EmployerPermission


class VacancyAPIView(generics.ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer


class VacancyListCreateView(generics.ListCreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [EmployerPermission]

    def perform_create(self, serializer):
        serializer.save(name_company=self.request.user.employer)
