from django.db import models

from Resumes.models import Resume
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

    company = models.ForeignKey(to=Employer, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    salary = models.IntegerField()
    description = models.TextField()
    time_of_creation = models.DateTimeField(auto_now=True)
    education = models.CharField(max_length=1, choices=CHOICES_EDUCATION)
    schedule = models.CharField(max_length=1, choices=CHOICES_SCHEDULE)

    def __str__(self):
        return f'{self.company},{self.job_title},{self.salary}'


class VacancyResponse(models.Model):
    applicant = models.ForeignKey(to=Applicant, on_delete=models.CASCADE, related_name='sent_response')
    employer = models.ForeignKey(to=Employer, on_delete=models.CASCADE, related_name='received_response')
    vacancy = models.ForeignKey(to=Vacancy, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    resume = models.ForeignKey(to=Resume, default=None, on_delete=models.CASCADE, related_name='resume_response')
