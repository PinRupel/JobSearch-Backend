from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase

from Users.models import User, Applicant
from Users.serializers import ApplicantRegisterSerializer, EmployerRegisterSerializer


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
