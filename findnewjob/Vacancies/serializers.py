from rest_framework import serializers

from Resumes.models import Resume
from .models import Vacancy, VacancyResponse


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = (
            'name_company',
            'job_title',
            'salary',
            'description',
            'time_of_creation',
            'education',
            'schedule')
        read_only_fields = ('name_company',)


class CustomResumeForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return Resume.objects.filter(user_id=self.context.get('request').user.id)


class VacancyResponseSerializer(serializers.ModelSerializer):
    resume = CustomResumeForeignKey()

    class Meta:
        model = VacancyResponse
        fields = "__all__"
        read_only_fields = ['applicant_id', 'employer_id', 'vacancy', 'status']
