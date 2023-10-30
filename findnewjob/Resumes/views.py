from rest_framework import viewsets
from .models import Resume
from Resumes.serializers import ResumeSerializer
from .permission import ResumePermission


class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [ResumePermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.applicant)
