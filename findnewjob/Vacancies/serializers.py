from rest_framework import serializers

from Users.serializers import EmployerSerializer

from .models import Vacancy


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = (
            'name_company',
            'job_title',
            'salary',
            'description',
            'education',
            'schedule')
        read_only_fields = ('time_of_creation', 'name_company',)
