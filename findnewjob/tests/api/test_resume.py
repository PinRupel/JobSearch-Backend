from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from Resumes.models import Resume
from Resumes.serializers import ResumeSerializer
from Users.models import User, Applicant


class ResumeAPITestCase(APITestCase):
    def setUp(self):
        self.resumes_data = [{
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
            'country_of_citizenship': 'Russia'},
            {
                'first_name': 'Alexey',
                'surname': 'Petrov',
                'last_name': 'Igorevich',
                'gender': 'M',
                'profession': 'Data Scientist',
                'experience': 5,
                'desire_salary': 150,
                'birth_date': '1988-09-10',
                'phone': '89998887766',
                'about_me': 'Data scientist with expertise in machine learning and statistical analysis.',
                'city': 'Saint Petersburg',
                'country_of_citizenship': 'Russia'
            },
            {
                'first_name': 'Elena',
                'surname': 'Sidorova',
                'last_name': 'Alexandrovna',
                'gender': 'F',
                'profession': 'Marketing Specialist',
                'experience': 7,
                'desire_salary': 90,
                'birth_date': '1985-03-25',
                'phone': '89761234567',
                'about_me': 'Experienced marketing professional with a focus on digital marketing strategies.',
                'city': 'Novosibirsk',
                'country_of_citizenship': 'Russia'
            },
            {
                'first_name': 'Igor',
                'surname': 'Kuznetsov',
                'last_name': 'Dmitrievich',
                'gender': 'M',
                'profession': 'Software Engineer',
                'experience': 4,
                'desire_salary': 130,
                'birth_date': '1992-11-05',
                'phone': '89654321098',
                'about_me': 'Passionate software engineer with a strong background in web development.',
                'city': 'Yekaterinburg',
                'country_of_citizenship': 'Russia'
            },
            {
                'first_name': 'Natalia',
                'surname': 'Popova',
                'last_name': 'Vladimirovna',
                'gender': 'F',
                'profession': 'Graphic Designer',
                'experience': 6,
                'desire_salary': 110,
                'birth_date': '1987-07-12',
                'phone': '89994443322',
                'about_me': 'Creative graphic designer with a keen eye for detail and a passion for visual aesthetics.',
                'city': 'Krasnoyarsk',
                'country_of_citizenship': 'Russia'
            },
            {
                'first_name': 'Sergey',
                'surname': 'Kovalev',
                'last_name': 'Ivanovich',
                'gender': 'M',
                'profession': 'Network Administrator',
                'experience': 8,
                'desire_salary': 140,
                'birth_date': '1980-04-30',
                'phone': '89887776655',
                'about_me': 'Experienced network administrator with expertise in maintaining and optimizing IT infrastructure.',
                'city': 'Samara',
                'country_of_citizenship': 'Russia'
            }
        ]
        self.user = User.objects.create_user(email='vadim@mail.ru', is_applicant=True, password='test')
        self.applicant = Applicant.objects.create(user=self.user, first_name='vadim', last_name='gilimzianov',
                                                  email='vadim@mial.ru')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_resume(self):
        self.responses = []
        for data in self.resumes_data:
            self.responses.append(self.client.post(reverse('Resume:resume-list'), data))

        for i in range(len(self.responses)):
            self.assertEqual(self.responses[i].status_code, 201)
            self.assertEqual(self.responses[i].data['first_name'], self.resumes_data[i]['first_name'])
            self.assertEqual(self.responses[i].data['surname'], self.resumes_data[i]['surname'])
            self.assertEqual(self.responses[i].data['last_name'], self.resumes_data[i]['last_name'])
            self.assertEqual(self.responses[i].data['gender'], self.resumes_data[i]['gender'])
            self.assertEqual(self.responses[i].data['profession'], self.resumes_data[i]['profession'])
            self.assertEqual(self.responses[i].data['experience'], self.resumes_data[i]['experience'])
            self.assertEqual(self.responses[i].data['desire_salary'], self.resumes_data[i]['desire_salary'])
            self.assertEqual(self.responses[i].data['birth_date'], self.resumes_data[i]['birth_date'])
            self.assertEqual(self.responses[i].data['phone'], self.resumes_data[i]['phone'])
            self.assertEqual(self.responses[i].data['about_me'], self.resumes_data[i]['about_me'])
            self.assertEqual(self.responses[i].data['city'], self.resumes_data[i]['city'])
            self.assertEqual(self.responses[i].data['country_of_citizenship'],
                             self.resumes_data[i]['country_of_citizenship'])

    def test_filter_resume(self):
        url = reverse('Resume:resume-list')

        for data in self.resumes_data:
            self.client.post(url, data)

        filter_data_city = {
            'city': 'Kazan'
        }
        filter_by_date = {
            'birth_date_after': '1990-01-01',
            'birth_date_before': '2000-01-01'
        }
        filter_data_exp = {
            'experience_min': 2,
        }

        resume_by_city = Resume.objects.filter(city=filter_data_city['city'])
        resume_by_birth = Resume.objects.filter(birth_date__gte=filter_by_date['birth_date_after'],
                                                birth_date__lte=filter_by_date['birth_date_before'])
        resume_by_exp = Resume.objects.filter(experience__gte=filter_data_exp['experience_min'])

        response_by_city = self.client.get(url, filter_data_city)
        response_by_birth = self.client.get(url, filter_by_date)
        response_by_exp = self.client.get(url, filter_data_exp)

        serializer_data_city = ResumeSerializer(resume_by_city, many=True).data
        serializer_data_birth = ResumeSerializer(resume_by_birth, many=True).data
        serializer_data_exp = ResumeSerializer(resume_by_exp, many=True).data

        self.assertEqual(response_by_city.status_code, 200)
        self.assertEqual(response_by_birth.status_code, 200)
        self.assertEqual(response_by_exp.status_code, 200)

        self.assertEqual(response_by_city.data, serializer_data_city)
        self.assertEqual(response_by_birth.data, serializer_data_birth)
        self.assertEqual(response_by_exp.data, serializer_data_exp)

    def test_get_resume(self):
        self.client.post(reverse('Resume:resume-list'), self.resumes_data[0])
        response = self.client.get(reverse('Resume:resume-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['first_name'], self.resumes_data[0]['first_name'])
        self.assertEqual(response.data[0]['surname'], self.resumes_data[0]['surname'])
        self.assertEqual(response.data[0]['last_name'], self.resumes_data[0]['last_name'])
        self.assertEqual(response.data[0]['gender'], self.resumes_data[0]['gender'])
        self.assertEqual(response.data[0]['profession'], self.resumes_data[0]['profession'])
        self.assertEqual(response.data[0]['experience'], self.resumes_data[0]['experience'])
        self.assertEqual(response.data[0]['desire_salary'], self.resumes_data[0]['desire_salary'])
        self.assertEqual(response.data[0]['birth_date'], self.resumes_data[0]['birth_date'])
        self.assertEqual(response.data[0]['phone'], self.resumes_data[0]['phone'])
        self.assertEqual(response.data[0]['about_me'], self.resumes_data[0]['about_me'])
        self.assertEqual(response.data[0]['city'], self.resumes_data[0]['city'])
        self.assertEqual(response.data[0]['country_of_citizenship'], self.resumes_data[0]['country_of_citizenship'])

    def test_delete_resume(self):
        response_del = self.client.post(reverse('Resume:resume-list'), self.resumes_data[0])
        self.assertEqual(response_del.status_code, 201)
        resume_id = response_del.data.get('id')
        delete_url = reverse('Resume:resume-detail', kwargs={'pk': resume_id})
        delete_response = self.client.delete(delete_url)
        self.assertEqual(delete_response.status_code, 204)
        response_after_delete = self.client.get(delete_url)
        self.assertEqual(response_after_delete.status_code, 404)

    def test_put_patch_resume(self):
        create_response = self.client.post(reverse('Resume:resume-list'), self.resumes_data[0])
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