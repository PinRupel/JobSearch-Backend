from django.urls import path, include
from rest_framework import routers
from Vacancies.views import VacancyAPIViewSet, VacancyResponseAPIViewSet, GetVacancyResponseAPIView

app_name = 'Vacancies'

router = routers.DefaultRouter()
router.register(r'vacancies', VacancyAPIViewSet)
router.register(r'response', VacancyResponseAPIViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('vacancies/response/<int:pk>/', GetVacancyResponseAPIView.as_view(), name='vacancy-response')
]
