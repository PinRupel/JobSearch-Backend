from django.urls import path, include
from rest_framework import routers

from .views import *

app_name = 'Users'

router = routers.DefaultRouter()
router.register(r'applicant', ApplicantViewSet)
router.register(r'employer', EmployerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/applicant/', ApplicantRegisterApiView.as_view(), name='applicant-register'),
    path('register/employer/', EmployerRegisterApiView.as_view(), name='employer-register'),
]
