from django.db import models

from Users.models import Applicant, Employer


class Resume(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]

    user = models.ForeignKey(to=Applicant, on_delete=models.CASCADE, related_name='applicant')
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    profession = models.CharField(max_length=100)
    experience = models.IntegerField(default=0)
    desire_salary = models.PositiveIntegerField()
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    about_me = models.TextField(blank=True)
    city = models.CharField(max_length=150)
    country_of_citizenship = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class ResumeInvitation(models.Model):
    sender = models.ForeignKey(to=Employer, on_delete=models.CASCADE, related_name='sent_invetion')
    recipient = models.ForeignKey(to=Applicant, on_delete=models.CASCADE, related_name='get_invetion')
    resume = models.ForeignKey(to=Resume, on_delete=models.CASCADE)
    message = models.TextField()
