from rest_framework import serializers

from .models import Resume


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = (
            'first_name',
            'last_name',
            'surname',
            'last_name',
            'gender',
            'profession',
            'experience',
            'desire_salary',
            'birth_date',
            'phone',
            'about_me',
            'city',
            'country_of_citizenship',
        )
        read_only_fieldz = ('user',)
