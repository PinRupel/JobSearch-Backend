from rest_framework.test import APITestCase
from django.urls import reverse

from Users.models import User, Applicant, Employer
from rest_framework.authtoken.models import Token


class IsApplicantOrReadOnlyTest(APITestCase):

    def setUp(self):
        self.new_data = {'first_name': 'New_name',
                         'last_name': 'New_last_name',
                         'email': 'new@test.ru'}
        self.user = User.objects.create_user(email='test@test.ru', is_applicant=True, password='TestPass1234')
        self.applicant = Applicant.objects.create(first_name='Test', last_name='Test', email='test@test.ru',
                                                  user=self.user)

        self.other_user = User.objects.create_user(email='test_other@test.ru', is_applicant=True,
                                                   password='TestPass1234')
        self.applicant_other = Applicant.objects.create(first_name='Test_other', last_name='Test',
                                                        email='test_other@test.ru',
                                                        user=self.other_user)

        self.user_employer = User.objects.create(email='test_e@test.ru', is_employer=True, password='TestPass123')
        self.employer = Employer.objects.create(company_name='company_name', email='test_e@test.ru',
                                                user=self.user_employer)

    def test_get_permission(self):
        self.response_get = self.client.get(reverse('Users:applicant-detail', kwargs={'pk': self.user.id}))

        self.assertEqual(self.response_get.status_code, 200)

    def test_unauthorized(self):
        self.response_put = self.client.put(reverse('Users:applicant-detail', kwargs={'pk': self.user.id}))
        self.response_patch = self.client.patch(reverse('Users:applicant-detail', kwargs={'pk': self.user.id}))

        self.assertEqual(self.response_put.status_code, 401)
        self.assertEqual(self.response_patch.status_code, 401)

    def test_permission_denied(self):
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.response_put_other = self.client.put(reverse('Users:applicant-detail', kwargs={'pk': self.other_user.id}),
                                                  self.new_data)
        self.response_patch_other = self.client.patch(
            reverse('Users:applicant-detail', kwargs={'pk': self.other_user.id}),
            self.new_data)

        self.assertEqual(self.response_put_other.status_code, 403)
        self.assertEqual(self.response_patch_other.status_code, 403)

        self.token = Token.objects.create(user=self.user_employer)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.response_put_employer = self.client.put(
            reverse('Users:applicant-detail', kwargs={'pk': self.other_user.id}),
            self.new_data)
        self.response_patch_employer = self.client.patch(
            reverse('Users:applicant-detail', kwargs={'pk': self.other_user.id}),
            self.new_data)

        self.assertEqual(self.response_put_employer.status_code, 403)
        self.assertEqual(self.response_patch_employer.status_code, 403)

    def test_permission_granted(self):
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.response_put = self.client.put(reverse('Users:applicant-detail', kwargs={'pk': self.user.id}),
                                            self.new_data)
        self.response_patch = self.client.patch(reverse('Users:applicant-detail', kwargs={'pk': self.user.id}),
                                                self.new_data)

        self.assertEqual(self.response_put.status_code, 200)
        self.assertEqual(self.response_patch.status_code, 200)


class IsEmployerOrReadOnlyTest(APITestCase):
    def setUp(self) -> None:
        self.new_data = {'company_name': 'New_name',
                         'email': 'new@test.ru'}

        self.user_employer = User.objects.create_user(email='test_e@test.ru', is_employer=True, password='TestPass123')
        self.employer = Employer.objects.create(company_name='company_name', email='test_e@test.ru',
                                                user=self.user_employer)

        self.other_user_employer = User.objects.create_user(email='test@test.ru', is_employer=True,
                                                            password='TestPass123')
        self.other_employer = Employer.objects.create(company_name='company_name', email='test@test.ru',
                                                      user=self.other_user_employer)

        self.other_user_applicant = User.objects.create_user(email='test_other@test.ru', is_applicant=True,
                                                             password='TestPass1234')
        self.applicant_other = Applicant.objects.create(first_name='Test_other', last_name='Test',
                                                        email='test_other@test.ru',
                                                        user=self.other_user_applicant)

    def test_get_permission(self):
        self.response_get = self.client.get(reverse('Users:employer-detail', kwargs={'pk': self.user_employer.id}))

        self.assertEqual(self.response_get.status_code, 200)

    def test_unauthorized(self):
        self.response_put = self.client.put(reverse('Users:employer-detail', kwargs={'pk': self.user_employer.id}),
                                            self.new_data)
        self.response_patch = self.client.patch(reverse('Users:employer-detail', kwargs={'pk': self.user_employer.id}),
                                                self.new_data)

        self.assertEqual(self.response_put.status_code, 401)
        self.assertEqual(self.response_patch.status_code, 401)

    def test_permission_denied(self):
        self.token = Token.objects.create(user=self.user_employer)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.response_put = self.client.put(
            reverse('Users:employer-detail', kwargs={'pk': self.other_user_employer.id}),
            self.new_data)
        self.response_patch = self.client.patch(
            reverse('Users:employer-detail', kwargs={'pk': self.other_user_employer.id}),
            self.new_data)

        self.assertEqual(self.response_put.status_code, 403)
        self.assertEqual(self.response_patch.status_code, 403)

        self.token = Token.objects.create(user=self.other_user_applicant)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.response_put = self.client.put(
            reverse('Users:employer-detail', kwargs={'pk': self.user_employer.id}),
            self.new_data)
        self.response_patch = self.client.patch(
            reverse('Users:employer-detail', kwargs={'pk': self.user_employer.id}),
            self.new_data)

        self.assertEqual(self.response_put.status_code, 403)
        self.assertEqual(self.response_patch.status_code, 403)

    def test_permission_granted(self):
        self.token = Token.objects.create(user=self.user_employer)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.response_put = self.client.put(
            reverse('Users:employer-detail', kwargs={'pk': self.user_employer.id}),
            self.new_data)
        self.response_patch = self.client.patch(
            reverse('Users:employer-detail', kwargs={'pk': self.user_employer.id}),
            self.new_data)

        self.assertEqual(self.response_put.status_code, 200)
        self.assertEqual(self.response_patch.status_code, 200)