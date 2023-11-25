from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from Users.models import User, Employer


# from Resumes.models import Resume


class TestResumePermission(APITestCase):

    def test_create_resume_unauthenticated(self):
        resumes_data = {
            'first_name': 'Vadim',
            'surname': 'Gilimzianov',
            'last_name': 'Radisovich',
            'gender': 'M',
            'profession': 'TestProf',
            'experience': 1,
            'desire_salary': 100,
            'birth_date': '1999-02-20',
            'phone': '89951338376',
            'about_me': 'TestText',
            'city': 'Kazan',
            'country_of_citizenship': 'Russia'
        }

        create_response = self.client.post(reverse('Resume:resume-list'), resumes_data)

        self.assertEqual(create_response.status_code, 401)

    def test_create_resume_for_employer(self):
        resumes_data = {
            'first_name': 'Vadim',
            'surname': 'Gilimzianov',
            'last_name': 'Radisovich',
            'gender': 'M',
            'profession': 'TestProf',
            'experience': 1,
            'desire_salary': 100,
            'birth_date': '1999-02-20',
            'phone': '89951338376',
            'about_me': 'TestText',
            'city': 'Kazan',
            'country_of_citizenship': 'Russia'
        }

        self.user = User.objects.create_user(email='vadim@mail.ru', is_employer=True, password='test')
        self.applicant = Employer.objects.create(user=self.user, company_name='vadim', email='vadim@mial.ru')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.post(reverse('Resume:resume-list'), resumes_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
