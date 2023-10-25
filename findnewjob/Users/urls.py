from django.urls import path, include
from rest_framework import routers

from .views import *

app_name = 'Users'

router_applicant = routers.DefaultRouter()
router_applicant.register(r'applicant', ApplicantViewSet)
router_employer = routers.DefaultRouter()
router_employer.register(r'employer', EmployerViewSet)

urlpatterns = [
    path('registr/applicant/', ApplicantRegisterApiView.as_view(), name='applicant-register'),
    path('registr/employer/', EmployerRegisterApiView.as_view(), name='employer-register'),
    path('', include(router_applicant.urls)),
    path('', include(router_employer.urls))
]
