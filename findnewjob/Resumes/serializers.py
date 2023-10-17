from rest_framework import serializers

from Resumes.models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ('first_name', 'last_name')
