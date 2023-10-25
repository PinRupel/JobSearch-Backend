from rest_framework import serializers
from Users.models import User, Applicant, Employer
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'is_applicant', 'is_employer')


class ApplicantRegisterSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True,
                                     style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True,
                                      style={'input_type': 'password'})
    date_joined = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return super().validate(attrs)

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
        )
        user.is_applicant = True
        user.set_password(validated_data['password'])
        user.save()
        applicant = Applicant(first_name=validated_data['first_name'],
                              last_name=validated_data['last_name'],
                              email=validated_data['email'],
                              user=user)
        applicant.save()
        return applicant


class EmployerRegisterSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    company_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True,
                                     style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    date_joined = serializers.DateTimeField(read_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
        )
        user.is_employer = True
        user.set_password(validated_data['password'])
        user.save()
        employer = Employer(company_name=validated_data['company_name'],
                            email=validated_data['email'],
                            user=user)
        employer.save()
        return employer


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ('user', 'first_name', 'last_name', 'email')
        read_only_fields = ['user']

    def update(self, instance, validated_data):
        user = User.objects.get(id=instance.pk)
        user.email = validated_data.get('email', user.email)
        user.save()
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ('user', 'company_name', 'email')
        read_only_fields = ['user']

    def update(self, instance, validated_data):
        user = User.objects.get(id=instance.pk)
        user.email = validated_data.get('email', user.email)
        user.save()
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance