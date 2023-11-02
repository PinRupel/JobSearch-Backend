from django.urls import path, include
from rest_framework import routers
from Vacancies.views import VacancyAPIViewSet

app_name = 'Vacancies'

router = routers.DefaultRouter()
router.register(r'vacancies', VacancyAPIViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
