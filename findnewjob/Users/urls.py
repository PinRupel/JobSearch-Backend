from django.urls import path
from .views import *

app_name = 'Users'

urlpatterns = [
    path('for_applicants/', ApplicantRegisterApiView.as_view(), name='applicant-register'),
    path('for_employers/', EmployerRegisterApiView.as_view(), name='employer-register')
]
