from django.conf import settings
from django.core.mail import send_mail


def send_email(subject,message,user):
    """
        sending email to user 
        
        Arguments:
            subject,message,user
    """
    send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER,
    [user.email]
)
