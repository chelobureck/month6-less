from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from decouple import config


@shared_task
def add(x, y):
    return x + y

@shared_task
def send_otp(email, code):
    send_mail(
        'OTP for registration',
        f'Your OTP is {code}',
        config('EMAIL_HOST_USER'), # type: ignore
        [email],
        fail_silently=False,
    )