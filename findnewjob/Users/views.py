from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from Users.models import Applicant, Employer, ActivationKey
from Users.permissions import IsCurApplicantOrReadOnly, IsCurEmployerOrReadOnly
from Users.serializers import ApplicantRegisterSerializer, EmployerRegisterSerializer, ApplicantSerializer, \
    EmployerSerializer
from Users.utils import Verify


class VerifyEmail(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        activation_code = kwargs.get('activation_code')

        code_object = get_object_or_404(ActivationKey, code=activation_code)

        if not code_object.is_active:
            return Response({'error': 'Ссылка более неактивна'}, status=status.HTTP_400_BAD_REQUEST)

        user = code_object.user
        user.is_verified = True
        user.save()

        code_object.is_active = False
        code_object.save()

        return Response({'success': 'Учетная запись подтверждена'}, status=status.HTTP_200_OK)


class ApplicantRegisterApiView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ApplicantRegisterSerializer

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {'error': 'Пользователь с таким Email уже существует, ссылка для подтверждения направлена повторно'},
                status=status.HTTP_400_BAD_REQUEST)
        finally:
            Verify.send_email_activate(request)
        return response


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
