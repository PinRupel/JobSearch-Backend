from django.db import transaction
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase

from Users.models import User, Applicant, Employer
from Users.serializers import ApplicantRegisterSerializer, EmployerRegisterSerializer

from rest_framework.authtoken.models import Token


class EmployerRegisterSerializerTest(TestCase):

    def setUp(self) -> None:
        self.payload = {
            'company_name': 'test_company',
            'email': 'some_email@test.ru',
            'password': 'TestingPassword1234567',
            'password2': 'TestingPassword1234567',
        }
        self.serializer = EmployerRegisterSerializer(data=self.payload)

    def test_ok(self):
        self.assertTrue(self.serializer.is_valid())


class EmployerRegisterApiTestCase(APITestCase):

    def setUp(self) -> None:
        self.payload = {
            'company_name': 'test_company',
            'email': 'some_email@test.ru',
            'password': 'TestingPassword1234567',
            'password2': 'TestingPassword1234567',
        }
        self.response = self.client.post(reverse("Users:employer-register"), self.payload)

    def test_create(self):
        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data.get('user')['email'], self.payload['email'])
        self.assertFalse(self.response.data.get('user')['is_applicant'])
        self.assertTrue(self.response.data.get('user')['is_employer'])
        self.assertEqual(self.response.data.get('company_name'), self.payload['company_name'])
        self.assertEqual(self.response.data.get('email'), self.payload['email'])


class ApplicantRegisterSerializerTest(TestCase):

    def setUp(self) -> None:
        self.payload = {
            'first_name': 'Test_name',
            'last_name': 'Test_last_name',
            'email': 'some_email@test.ru',
            'password': 'TestingPassword1234567',
            'password2': 'TestingPassword1234567',
        }
        self.serializer = ApplicantRegisterSerializer(data=self.payload)

    def test_ok(self):
        self.assertTrue(self.serializer.is_valid())


class ApplicantRegisterApiTestCase(APITestCase):

    def setUp(self) -> None:
        self.payload = {
            'first_name': 'Test_name',
            'last_name': 'Test_last_name',
            'email': 'some_email@test.ru',
            'password': 'TestingPassword1234567',
            'password2': 'TestingPassword1234567',
        }
        self.response = self.client.post(reverse("Users:applicant-register"), self.payload)

    def test_create(self):
        self.assertEqual(self.response.status_code, 201)
        self.assertEqual(self.response.data.get('user')['email'], self.payload['email'])
        self.assertTrue(self.response.data.get('user')['is_applicant'])
        self.assertFalse(self.response.data.get('user')['is_employer'])
        self.assertEqual(self.response.data.get('first_name'), self.payload['first_name'])
        self.assertEqual(self.response.data.get('last_name'), self.payload['last_name'])
        self.assertEqual(self.response.data.get('email'), self.payload['email'])


class ApplicantUpdateApiTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(email='test@test.ru', is_applicant=True, password='TestingPassword1234')
        self.applicant = Applicant.objects.create(first_name='first_name', last_name='last_name', email='test@test.ru',
                                                  user=self.user)
        self.payload = {
            'first_name': 'Update_name',
            'last_name': 'Update_last_name',
            'email': 'update_email@test.ru'
        }
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.response_patch = self.client.patch(reverse("Users:applicant-detail", kwargs={'pk': self.applicant.user_id}), self.payload)

    def test_update_patch(self):
        self.assertEqual(self.response_patch.status_code, 200)
        self.assertEqual(self.response_patch.data.get('user'), self.applicant.user_id)
        self.assertEqual(self.response_patch.data.get('first_name'), self.payload.get('first_name'))
        self.assertEqual(self.response_patch.data.get('last_name'), self.payload.get('last_name'))
        self.assertEqual(self.response_patch.data.get('email'), self.payload.get('email'))


class EmployerUpdateApiTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(email='test@test.ru', is_employer=True, password='TestingPassword1234')
        self.employer = Employer.objects.create(company_name='company_name', email='test@test.ru',
                                                user=self.user)
        self.payload = {
            'company_name': 'Update_name',
            'email': 'update_email@test.ru'
        }
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.response_patch = self.client.patch(
            reverse("Users:employer-detail", kwargs={'pk': self.employer.user_id}), self.payload)

    def test_update_patch(self):
        self.assertEqual(self.response_patch.status_code, 200)
        self.assertEqual(self.response_patch.data.get('user'), self.employer.user_id)
        self.assertEqual(self.response_patch.data.get('company_name'), self.payload.get('company_name'))
        self.assertEqual(self.response_patch.data.get('email'), self.payload.get('email'))
