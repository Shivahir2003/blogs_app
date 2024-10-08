from django.conf import settings
from django.core.mail import EmailMultiAlternatives

def send_email(subject,html_content,text_content,user):
    """
        sending email to user 
        
        Arguments:
            subject,html_content,text_content,user
    """
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email,]
    email=EmailMultiAlternatives(subject,text_content,email_from,recipient_list)
    email.attach_alternative(html_content,'text/html')
    email.send()

def send_mail_to_multiple(subject,text_content,html_content,user_emails):
    """
        sending email to multiple user user
        
        Arguments:
            subject,text_content,html_content,user_email
            
    """
    email_from = settings.EMAIL_HOST_USER
    recipient_list = user_emails
    email=EmailMultiAlternatives(subject,text_content,email_from,recipient_list)
    email.attach_alternative(html_content,'text/html')
    email.send()
