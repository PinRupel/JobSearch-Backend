from django.urls import path
from .views import *

app_name = 'Users'

urlpatterns = [
    path('registr/applicant/', ApplicantRegisterApiView.as_view(), name='applicant-register'),
    path('registr/employer/', EmployerRegisterApiView.as_view(), name='employer-register'),
    path('applicant/profile/<int:pk>/', ApplicantProfileApiView.as_view(), name='applicant_profile'),
    path('employer/profile/<int:pk>/', EmployerProfileApiView.as_view(), name='employer_profile'),
    path('applicant/profile/<int:pk>/edit/', ApplicantUpdateApiView.as_view(), name='applicant_profile_edit'),
    # path('employer/profile/<int:pk>/edit/', EmployerUpdateApiView.as_view(), name='employer_profile_edit')
]
