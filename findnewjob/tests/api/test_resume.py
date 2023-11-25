from django.urls import reverse
from rest_framework.authtoken.models import Token
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
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.response = self.client.post(reverse('Resume:resume-list'), self.resumes_data)

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

    def test_get_resume(self):
        self.client.post(reverse('Resume:resume-list'), self.resumes_data)
        response = self.client.get(reverse('Resume:resume-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['first_name'], self.resumes_data['first_name'])
        self.assertEqual(response.data[0]['surname'], self.resumes_data['surname'])
        self.assertEqual(response.data[0]['last_name'], self.resumes_data['last_name'])
        self.assertEqual(response.data[0]['gender'], self.resumes_data['gender'])
        self.assertEqual(response.data[0]['profession'], self.resumes_data['profession'])
        self.assertEqual(response.data[0]['experience'], self.resumes_data['experience'])
        self.assertEqual(response.data[0]['desire_salary'], self.resumes_data['desire_salary'])
        self.assertEqual(response.data[0]['birth_date'], self.resumes_data['birth_date'])
        self.assertEqual(response.data[0]['phone'], self.resumes_data['phone'])
        self.assertEqual(response.data[0]['about_me'], self.resumes_data['about_me'])
        self.assertEqual(response.data[0]['city'], self.resumes_data['city'])
        self.assertEqual(response.data[0]['country_of_citizenship'], self.resumes_data['country_of_citizenship'])

    def test_delete_resume(self):
        response_del = self.client.post(reverse('Resume:resume-list'), self.resumes_data)
        self.assertEqual(response_del.status_code, 201)
        resume_id = response_del.data.get('id')
        delete_url = reverse('Resume:resume-detail', kwargs={'pk': resume_id})
        delete_response = self.client.delete(delete_url)
        self.assertEqual(delete_response.status_code, 204)
        response_after_delete = self.client.get(delete_url)
        self.assertEqual(response_after_delete.status_code, 404)

    def test_put_patch_resume(self):
        create_response = self.client.post(reverse('Resume:resume-list'), self.resumes_data)
        self.assertEqual(create_response.status_code, 201)
        resume_id = create_response.data.get('id')

        update_resume = {
            'first_name': 'PutVadim',
            'surname': 'PutGilimzianov',
            'last_name': 'PutRadisovich',
            'gender': 'F',
            'profession': 'PutTestProf',
            'experience': 2,
            'desire_salary': 200,
            'birth_date': '1991-01-10',
            'phone': '88005553535',
            'about_me': 'PutTestText',
            'city': 'PutKazan',
            'country_of_citizenship': 'PutRussia'
        }

        put_url = reverse('Resume:resume-detail', args=[resume_id])
        put_response = self.client.put(put_url, update_resume)
        self.assertEqual(put_response.status_code, 200)
        self.assertEqual(put_response.data['first_name'], update_resume['first_name'])
        self.assertEqual(put_response.data['surname'], update_resume['surname'])
        self.assertEqual(put_response.data['last_name'], update_resume['last_name'])
        self.assertEqual(put_response.data['gender'], update_resume['gender'])
        self.assertEqual(put_response.data['profession'], update_resume['profession'])
        self.assertEqual(put_response.data['experience'], update_resume['experience'])
        self.assertEqual(put_response.data['desire_salary'], update_resume['desire_salary'])
        self.assertEqual(put_response.data['birth_date'], update_resume['birth_date'])
        self.assertEqual(put_response.data['phone'], update_resume['phone'])
        self.assertEqual(put_response.data['about_me'], update_resume['about_me'])
        self.assertEqual(put_response.data['city'], update_resume['city'])
        self.assertEqual(put_response.data['country_of_citizenship'], update_resume['country_of_citizenship'])

        patched_data = {
            'first_name': 'PatchVadim',
            'surname': 'PatchGilimzianov'
        }

        patch_response = self.client.patch(put_url, patched_data)
        self.assertEqual(patch_response.status_code, 200)
        self.assertEqual(patch_response.data['first_name'], patched_data['first_name'])
        self.assertEqual(patch_response.data['surname'], patched_data['surname'])


