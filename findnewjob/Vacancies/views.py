from django_filters.rest_framework import DjangoFilterBackend
from .filters import VacancyFilter
from rest_framework import viewsets, mixins, filters, generics
from rest_framework.generics import get_object_or_404
from .models import Vacancy, VacancyResponse
from Vacancies.serializers import VacancySerializer, VacancyResponseSerializer
from .permissions import VacancyPermission, ResponsePermission


class VacancyAPIViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [VacancyPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = VacancyFilter
    search_fields = ['job_title', 'company__company_name']

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.employer)


class VacancyResponseAPIViewSet(mixins.CreateModelMixin,
                                viewsets.GenericViewSet):
    queryset = VacancyResponse.objects.all()
    serializer_class = VacancyResponseSerializer
    permission_classes = [ResponsePermission]

    def perform_create(self, serializer):
        applicant_id = self.request.user.applicant
        vacancy = get_object_or_404(Vacancy, id=self.kwargs['pk'])
        employer_id = vacancy.company
        serializer.save(applicant_id=applicant_id, vacancy=vacancy, employer_id=employer_id)


class GetVacancyResponseAPIView(generics.RetrieveAPIView):
    queryset = VacancyResponse.objects.all()
    serializer_class = VacancyResponseSerializer
    permission_classes = [ResponsePermission]
