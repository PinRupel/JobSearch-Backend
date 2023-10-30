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

# class VacancyResponseAPIview(generics.CreateAPIView):
#     queryset = VacancyResponse.objects.all()
#     serializer_class = VacancyResponseSerializer
#     permission_classes = [ResponsePermission]
#
#     def perform_create(self, serializer):
#         sender = self.request.user.applicant
#         vacancy = Vacancy.objects.get_object_or_404(id=self.kwargs['pk'])
#         recipient = vacancy.name_company
#         serializer.save(sender=sender, vacancy=vacancy, recipient=recipient)
