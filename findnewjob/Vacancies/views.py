from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from .models import Vacancy
from Vacancies.serializers import VacancySerializer
from .permissions import VacancyPermission
from .filters import VacancyFilter


class VacancyAPIViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [VacancyPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = VacancyFilter
    search_fields = ['job_title', 'name_company__company_name']

    def perform_create(self, serializer):
        serializer.save(name_company=self.request.user.employer)
