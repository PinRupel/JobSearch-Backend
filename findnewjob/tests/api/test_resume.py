from django.urls import reverse
from rest_framework.test import APITestCase

from Users.models import User, Applicant


class ResumeAPITestCase(APITestCase):
    def setUp(self):
        self.resumes_data = {
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

        self.user = User.objects.create_user(email='vadim@mail.ru', is_applicant=True, password='test')
        self.applicant = Applicant.objects.create(user=self.user, first_name='vadim', last_name='gilimzianov',
                                                  email='vadim@mial.ru')
        self.client.login(email='vadim@mail.ru', password='test')
        self.response = self.client.post(reverse('create-resume'), self.resumes_data)

    def test_create_resume(self):
        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data['first_name'], self.resumes_data['first_name'])
        self.assertEqual(self.response.data['surname'], self.resumes_data['surname'])
        self.assertEqual(self.response.data['last_name'], self.resumes_data['last_name'])
        self.assertEqual(self.response.data['gender'], self.resumes_data['gender'])
        self.assertEqual(self.response.data['profession'], self.resumes_data['profession'])
        self.assertEqual(self.response.data['experience'], self.resumes_data['experience'])
        self.assertEqual(self.response.data['desire_salary'], self.resumes_data['desire_salary'])
        self.assertEqual(self.response.data['birth_date'], self.resumes_data['birth_date'])
        self.assertEqual(self.response.data['phone'], self.resumes_data['phone'])
        self.assertEqual(self.response.data['about_me'], self.resumes_data['about_me'])
        self.assertEqual(self.response.data['city'], self.resumes_data['city'])
        self.assertEqual(self.response.data['country_of_citizenship'], self.resumes_data['country_of_citizenship'])
