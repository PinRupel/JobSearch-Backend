from rest_framework import serializers
from .models import Vacancy


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
