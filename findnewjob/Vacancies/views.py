from django.shortcuts import render

from rest_framework import generics

from .models import Vacancy
from Vacancies.serializers import VacancySerializer, VacancyUpdateSerializer
from .permissions import EmployerUpdatePermissions, EmployerDeletePermissions, EmployerPermission


class VacancyAPIList(generics.ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer


class VacancyAPICreate(generics.ListCreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [EmployerPermission]

    def perform_create(self, serializer):
        serializer.save(name_company=self.request.user.employer)


class VacancyAPIUpdate(generics.UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer
    permission_classes = [EmployerUpdatePermissions]


class vacancyAPIDelete(generics.DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer
    permission_classes = [EmployerDeletePermissions]
