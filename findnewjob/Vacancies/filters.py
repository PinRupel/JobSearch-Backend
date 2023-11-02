import django_filters
from django_filters import rest_framework as filters
from .models import Vacancy


class VacancyFilter(filters.FilterSet):
    salary = filters.RangeFilter()
    time_of_creation = filters.IsoDateTimeFilter(field_name="time_of_creation", lookup_expr="lte")

    class Meta:
        model = Vacancy
        fields = ['salary', 'time_of_creation', 'education', 'schedule']
