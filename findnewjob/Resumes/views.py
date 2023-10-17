from django.shortcuts import render

from rest_framework import generics

from Resumes.models import Resume
from Resumes.serializers import ResumeSerializer


class ResumeAPIView(generics.ListAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
