from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings


def send_email(subject,message,user):
    send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER,
    [user.email]
)
