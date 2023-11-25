from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, generics, filters
from rest_framework.generics import get_object_or_404

from Resumes.serializers import ResumeSerializer, InvitationSerializer
from .filters import ResumeFilter
from .models import Resume, ResumeResponse
from .permission import ResumePermission, ResumeResponsePermission


class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [ResumePermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ResumeFilter
    search_fields = ['profession']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.applicant)


class ResumeResponseAPIViewSet(mixins.CreateModelMixin,
                               viewsets.GenericViewSet):
    queryset = ResumeResponse.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [ResumeResponsePermission]

    def perform_create(self, serializer):
        employer = self.request.user.employer
        resume = get_object_or_404(Resume, id=self.kwargs['pk'])
        applicant = resume.user
        serializer.save(employer=employer, resume=resume, applicant=applicant)


class GetResumeResponseAPIView(generics.RetrieveAPIView):
    queryset = ResumeResponse.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [ResumeResponsePermission]
