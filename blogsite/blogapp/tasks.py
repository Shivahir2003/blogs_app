from celery import shared_task
from django.contrib.auth.models import User

from django_celery_results.models import TaskResult

from blogapp.models import Blog
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from blogapp.utils import send_mail_to_multiple




@shared_task
def send_mail_for_new_blogs():
    if  Blog.objects.filter(created__date = timezone.now().date()).exists():
        users =User.objects.filter(is_superuser= False)
        blogs = Blog.objects.filter(created__date = timezone.now().date())
        user_emails =[]
        for user in users:
            user_emails.append(user.email)

        subject= f'Checkout new blog for today'
        html_content = render_to_string('email_templates/new_blog_email.html',{'blogs':blogs})
        text_content = strip_tags(html_content)
        send_mail_to_multiple(subject,text_content,html_content,user_emails)
        return "mail send for today"
    else :
        return "not blogs created today"


@shared_task()
def clear_task_result():
    TaskResult.objects.all().delete()
    return "all task deleted"
