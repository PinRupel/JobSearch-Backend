from rest_framework import serializers

from .models import Resume, ResumeResponse


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = (
            'id',
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
        read_only_fields = ('user', 'id',)


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeResponse
        fields = ('message',)
        read_only_fields = ('applicant', 'employer', 'resume',)
