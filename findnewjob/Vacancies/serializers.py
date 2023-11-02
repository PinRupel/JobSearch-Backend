from rest_framework import serializers
from .models import Vacancy


class VacancySerializer(serializers.ModelSerializer):
    time_of_creation = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", read_only=True)

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
