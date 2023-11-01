from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404

from .models import Vacancy, VacancyResponse
from Vacancies.serializers import VacancySerializer, VacancyResponseSerializer
from .permissions import VacancyPermission, ResponsePermission


class VacancyAPIViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [VacancyPermission]

    def perform_create(self, serializer):
        serializer.save(name_company=self.request.user.employer)


class VacancyResponseAPIViewSet(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    queryset = VacancyResponse.objects.all()
    serializer_class = VacancyResponseSerializer
    permission_classes = [ResponsePermission]

    def perform_create(self, serializer):
        applicant_id = self.request.user.applicant
        vacancy = get_object_or_404(Vacancy, id=self.kwargs['pk'])
        employer_id = vacancy.name_company
        serializer.save(applicant_id=applicant_id, vacancy=vacancy, employer_id=employer_id)
