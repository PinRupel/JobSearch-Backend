from rest_framework import generics
from rest_framework.permissions import AllowAny

from Users.models import Applicant, Employer
from Users.permissions import ApplicantPermission
from Users.serializers import ApplicantRegisterSerializer, EmployerRegisterSerializer, ApplicantSerializer, \
    EmployerSerializer


class ApplicantRegisterApiView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ApplicantRegisterSerializer


class EmployerRegisterApiView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmployerRegisterSerializer
    


class ApplicantProfileApiView(generics.RetrieveAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer


class ApplicantUpdateApiView(generics.RetrieveUpdateAPIView):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = (ApplicantPermission,)


# class EmployerUpdateApiView(generics.RetrieveUpdateAPIView):
#     queryset = Employer.objects.all()
#     serializer_class = EmployerSerializer
#     permission_classes = (EmployerPermission,)


class EmployerProfileApiView(generics.RetrieveAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
