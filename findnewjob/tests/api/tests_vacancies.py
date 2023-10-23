from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase

from Users.models import User, Employer


class VacancyAPITestCase(APITestCase):
    def setUp(self):
        self.vacancies_data = {
            'job_title': 'Test_job_title',
            'salary': 2000,
            'description': 'Test_description_bla_bla',
            'education': 'H',
            'schedule': 'F'
        }
        self.user = User.objects.create_user(email='vadim@mail.ru', is_employer=True, password='Test')
        self.employer = Employer.objects.create(user=self.user, company_name='Test', email='vadim@mail.ru')
        self.client.login(email='vadim@mail.ru', password='Test')
        self.response = self.client.post(reverse('create-vacancies'), self.vacancies_data)

    def test_create_vacancies(self):
        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data['job_title'], self.vacancies_data['job_title'])
        self.assertEqual(self.response.data['salary'], self.vacancies_data['salary'])
        self.assertEqual(self.response.data['description'], self.vacancies_data['description'])
        self.assertEqual(self.response.data['education'], self.vacancies_data['education'])
        self.assertEqual(self.response.data['schedule'], self.vacancies_data['schedule'])
