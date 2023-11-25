from django_filters import rest_framework as filters


class ResumeFilter(filters.FilterSet):
    experience_min = filters.NumberFilter(field_name="experience", lookup_expr="gte")
    city = filters.CharFilter(field_name="city", lookup_expr="icontains")
    birth_date = filters.DateFromToRangeFilter(field_name='birth_date')