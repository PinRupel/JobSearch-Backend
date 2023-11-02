from django.urls import path, include
from rest_framework import routers
from Vacancies.views import VacancyAPIViewSet, VacancyResponseAPIViewSet

app_name = 'Vacancies'

router = routers.DefaultRouter()
router.register(r'vacancies', VacancyAPIViewSet)

response_router = routers.DefaultRouter()
response_router.register(r'response', VacancyResponseAPIViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('vacancies/<int:pk>/', include(response_router.urls))
]
