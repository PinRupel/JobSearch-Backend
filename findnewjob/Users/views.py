from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import AllowAny

from Users.models import Applicant, Employer
from Users.permissions import IsCurApplicantOrReadOnly, IsCurEmployerOrReadOnly
from Users.serializers import ApplicantRegisterSerializer, EmployerRegisterSerializer, ApplicantSerializer, \
    EmployerSerializer


class ApplicantRegisterApiView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ApplicantRegisterSerializer


class EmployerRegisterApiView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmployerRegisterSerializer


class ApplicantViewSet(mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = (IsCurApplicantOrReadOnly,)



class EmployerViewSet(mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer
    permission_classes = (IsCurEmployerOrReadOnly,)
