from rest_framework import viewsets
from .models import Vacancy
from Vacancies.serializers import VacancySerializer
from .permissions import VacancyPermission


class VacancyAPIViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [VacancyPermission]

    def perform_create(self, serializer):
        serializer.save(name_company=self.request.user.employer)
