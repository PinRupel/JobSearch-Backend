from django.urls import reverse
from rest_framework import status

from Users.models import ActivationKey, User
from rest_framework.test import APITestCase


class VerifyEmailTestCase(APITestCase):

    def test_verification(self):
        self.user = User.objects.create_user(email='test@test.ru', password='TestingPassword1234')
        self.activation_code = ActivationKey.objects.create(user=self.user)
        self.assertFalse(self.user.is_verified)

        url = reverse('email-verify', kwargs={'activation_code': self.activation_code.code})
        response = self.client.get(url)

        self.user.refresh_from_db()
        self.activation_code.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.is_verified)
        self.assertFalse(self.activation_code.is_active)