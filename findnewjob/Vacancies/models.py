from django.db import models

from Users.models import Employer, Applicant


class Vacancy(models.Model):
    CHOICES_EDUCATION = [
        ('W', 'Без образования'),
        ('M', 'Среднее-специальное образование'),
        ('H', 'Высшее образование')
    ]

    CHOICES_SCHEDULE = [
        ('G', 'Гибкий график'),
        ('F', 'Пять / Два'),
        ('T', 'Два / Два')
    ]

    name_company = models.ForeignKey(to=Employer, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    salary = models.IntegerField()
    description = models.TextField()
    time_of_creation = models.DateTimeField(auto_now=True)
    education = models.CharField(max_length=1, choices=CHOICES_EDUCATION)
    schedule = models.CharField(max_length=1, choices=CHOICES_SCHEDULE)


class VacancyResponse(models.Model):
    sender = models.ForeignKey(to=Applicant, on_delete=models.CASCADE, related_name='sent_response')
    recipient = models.ForeignKey(to=Employer, on_delete=models.CASCADE, related_name='received_response')
    vacancy = models.ForeignKey(to=Vacancy, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    accepted = models.BooleanField(default=False)
