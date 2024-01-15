from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse

from Users.models import User, ActivationKey


class Verify:

    @staticmethod
    def send_email_activate(request):
        user_email = request.POST.get('email')
        user = User.objects.get(email=user_email)
        activation_code = ActivationKey.objects.get_or_create(user=user)
        domain = get_current_site()
        verify_link = reverse('email-verify', kwargs={'activation_code': activation_code[0].code})
        email = EmailMessage(
            subject='Активация аккаунта', body=f'Что бы активировать аккаунт перейдите по ссылке ниже \n  {verify_link}',
            to=[user_email])
        email.send()
