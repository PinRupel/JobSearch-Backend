from django.shortcuts import render

from rest_framework import generics

from Users.permissions import ApplicantPermission
from .models import Resume
from Resumes.serializers import ResumeSerializer


class ResumeAPIView(generics.CreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [ApplicantPermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.applicant)
