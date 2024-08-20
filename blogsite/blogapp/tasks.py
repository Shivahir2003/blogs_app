from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.core.cache import cache
from django.conf import settings

from openpyxl import Workbook
from celery import shared_task
from django_celery_results.models import TaskResult

from blogapp.utils import send_mail_to_multiple
from blogapp.models import Blog

@shared_task
def send_mail_for_new_blogs():
    """
        celery task for sending mail
        
        send mail to all users regarding to blogs created daily
    """
    if  Blog.objects.filter(created__date = timezone.now().date()).exists():
        blogs = Blog.objects.filter(created__date = timezone.now().date())
        users = User.objects.filter(is_superuser= False)
        for user in users:
            subject= f'Checkout new blog for today'
            html_content = render_to_string('email_templates/daily_blog_email.html',{'blogs':blogs})
            text_content = strip_tags(html_content)
            send_mail_to_multiple(subject,text_content,html_content,[user.email])
        return "mail send for today"
    else :
        return "not blogs created today"

@shared_task()
def clear_task_result():
    """
        celery task delete all task from database
    """
    TaskResult.objects.all().delete()
    return "all task deleted"

@shared_task()
def generate_blog_for_admin():
    """
        celery task for generate blog report for admin user
    """

    wb = Workbook()
    ws = wb.active
    ws.title = "Blogs_report"

    headers = ["Name","Author","Category","Created Date", "Created Time"]
    ws.append(headers)

    blogs = Blog.objects.all()
    for blog in blogs:
        ws.append([blog.title,blog.user.username,blog.categories.name,blog.created.strftime("%d/%m/%Y"),blog.created.strftime("%H:%M:%S %p")])

    wb.save(f"{settings.BASE_DIR}/reports/blog_reports.xlsx")
    cache.set("is_report_generated",True,timeout=60)

    return "generated blog reports"
