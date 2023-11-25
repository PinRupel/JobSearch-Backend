from rest_framework import serializers

from Resumes.models import Resume
from Users.serializers import EmployerSerializer
from .models import Vacancy, VacancyResponse


class VacancySerializer(serializers.ModelSerializer):
    time_of_creation = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", read_only=True)
    company = EmployerSerializer(read_only=True)

    class Meta:
        model = Vacancy
        fields = (
            'company',
            'job_title',
            'salary',
            'description',
            'time_of_creation',
            'education',
            'schedule')


class CustomResumeForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return Resume.objects.filter(user_id=self.context.get('request').user.id)


class VacancyResponseSerializer(serializers.ModelSerializer):
    resume = CustomResumeForeignKey()

    class Meta:
        model = VacancyResponse
        fields = "__all__"
        read_only_fields = ['applicant_id', 'employer_id', 'vacancy', 'status']
