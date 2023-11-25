from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from Vacancies.models import Vacancy
from Vacancies.serializers import VacancySerializer
from Users.models import User, Employer


class VacancyAPITestCase(APITestCase):
    def setUp(self):
        self.vacancies_data = [{
            'job_title': 'Test_job_title',
            'salary': 60000,
            'description': 'Test_description_bla_bla',
            'education': 'H',
            'schedule': 'F'
        },
            {
                'job_title': 'title',
                'salary': 40000,
                'description': 'Test_description_bla_bla',
                'education': 'M',
                'schedule': 'T'
            },
            {
                'job_title': 'Test',
                'salary': 80000,
                'description': 'Test_description_bla_bla',
                'education': 'H',
                'schedule': 'F'
            },
            {
                'job_title': 'another',
                'salary': 35000,
                'description': 'Test_description_bla_bla',
                'education': 'W',
                'schedule': 'T'
            },
            {
                'job_title': 'job',
                'salary': 110000,
                'description': 'Test_description_bla_bla',
                'education': 'H',
                'schedule': 'F'
            },
            {
                'job_title': 'another one',
                'salary': 11000,
                'description': 'Test_description_bla_bla',
                'education': 'H',
                'schedule': 'F'
            }]
        self.user = User.objects.create_user(email='vadim@mail.ru', is_employer=True, password='Test')
        self.employer = Employer.objects.create(user=self.user, company_name='company', email='vadim@mail.ru')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.response_1 = self.client.post(reverse('Vacancies:vacancy-list'), self.vacancies_data[0])
        for i in range(1, 6):
            self.client.post(reverse('Vacancies:vacancy-list'), self.vacancies_data[i])
        self.vacancies = Vacancy.objects.all()
        self.vacancies_filter = Vacancy.objects.filter(salary__gte=11000, salary__lte=60000, schedule='F',
                                                       education='H')
        self.vacancy_search_title = Vacancy.objects.filter(job_title__icontains='job')
        self.vacancy_search_company = Vacancy.objects.filter(company__company_name__icontains='company')

    def test_get(self):
        url = reverse('Vacancies:vacancy-list')
        self.response_get = self.client.get(url)
        serializer_data = VacancySerializer(self.vacancies, many=True).data
        self.assertEqual(self.response_get.status_code, 200)
        self.assertEqual(self.response_get.data, serializer_data)

    def test_post(self):
        self.assertEqual(self.response_1.status_code, 201)
        self.assertEqual(self.response_1.data['job_title'], self.vacancies_data[0]['job_title'])
        self.assertEqual(self.response_1.data['salary'], self.vacancies_data[0]['salary'])
        self.assertEqual(self.response_1.data['description'], self.vacancies_data[0]['description'])
        self.assertEqual(self.response_1.data['education'], self.vacancies_data[0]['education'])
        self.assertEqual(self.response_1.data['schedule'], self.vacancies_data[0]['schedule'])

    def test_filter(self):
        url = reverse('Vacancies:vacancy-list')
        self.response_filter = self.client.get(url, data={
            'education': 'H',
            'salary_min': '11000',
            'salary_max': '60000',
            'schedule': 'F'
        })
        serializer_data = VacancySerializer(self.vacancies_filter, many=True).data

        self.assertEqual(self.response_filter.status_code, 200)
        self.assertEqual(self.response_filter.data, serializer_data)

        self.response_search_title = self.client.get(url, data={
            'search': 'job'
        })
        self.response_search_company = self.client.get(url, data={
            'search': 'company'
        })

        search_serializer_title = VacancySerializer(self.vacancy_search_title, many=True).data
        search_serializer_company = VacancySerializer(self.vacancy_search_company, many=True).data

        self.assertEqual(self.response_search_title.status_code, 200)
        self.assertEqual(self.response_search_company.status_code, 200)

        self.assertEqual(self.response_search_title.data, search_serializer_title)
        self.assertEqual(self.response_search_company.data, search_serializer_company)
