from django.utils import timezone

from openpyxl import Workbook

from blogapp.models import Blog


def get_daily_blog_report():
    """ generate daily blog report """
    wb = Workbook()
    ws = wb.active
    ws.title = "daily_blog"

    headers = ["Name","Author","Category"]
    ws.append(headers)

    reported_time = timezone.now().strftime("%Y-%m-%d %H:%M")
    blogs = Blog.objects.filter(created__date = timezone.now().date())
    for blog in blogs:
        ws.append([blog.title,blog.user.username,blog.categories.name])

    wb.save(f"/home/shivahir/Videos/blogs report/daily_blog_reports_{reported_time}.xlsx")
