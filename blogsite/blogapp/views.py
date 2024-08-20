import requests
import os
from django.urls import reverse
from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.conf import settings
from django.http import HttpResponse
from django.core.cache import cache
from django.contrib.auth.decorators import login_required 

from blogapp.forms import BlogForm
from blogapp.models import Blog
from blogapp.tasks import generate_blog_for_admin
from blogapp.token import refresh_token_for_user

class BlogAppView(View):
    """ 
        Blog application class

        perfroms CRUD operations for blog application
    """

    def dispatch(self,request,**kwargs):
        if request.path == reverse("blogapp:blog_create"):
            return self.blog_add(request)
        elif request.path == reverse("blogapp:blog_dashboard"):
            return self.dashboard(request)
        elif request.path == reverse("blogapp:blog_category"):
            return self.blog_categories(request)
        elif request.path == reverse("blogapp:blog_myblogs"):
            return self.myblog_view(request)
        elif '/blogs/blog/details/'in request.path:
            return self.blog_details(request,**kwargs)
        elif '/blogs/blog/edit/'in request.path:
            return self.blog_edit(request,**kwargs)
        else:
            return redirect("blogapp:blog_dashboard")

    def dashboard(self,request):
        """
            blog dashboard Get method
            
            Arguments:
                request (HttpRequest)
            
            Returns:
                    render dashboard page with api call using ajax request
        """
        return render(request,'blogs/dashboard.html')

    def blog_add(self,request):
        """
            Add Blog for logged in user in Get method
            
            Arguments:
                request (HttpRequest)
            
            Required Parameters:
                title,description,post,category
                
            Optional Parameters:
                description
            
            Returns:
                In Get : render add Blog page with BlogForm
                In Post : Create Blog with api using ajax request
        """
        form = BlogForm()
        context = {
            "form": form
        }
        return render(request,'blogs/add_blog.html' ,context)

    def blog_edit(self,request,pk):
        """
            Edit Blog post method
            
            Arguments:
                request (HttpRequest)
                pk (primarykey)
            
            Required Parameters:
                title,post,category
                
            Optional Parameters:
                description

            Returns:
                In Get: 
                    render edit blog page 
                In Post:
                    edit blog with api using ajax request
        """
        blog=Blog.objects.get(pk=pk)
        form = BlogForm(instance=blog)
        context = {
            "form": form,
            "pk": pk
        }
        return render(request,'blogs/edit_blog.html' ,context)

    def blog_details(self,request,pk):
        """
            Show blog Details 
            
            Arguments:
                request (HttpRequest)
                pk      (primaryket)
            
            Returns:
                In Get : render blog detail using api request
        """
        url = f'{settings.URL_BLOG_DETAILS}{pk}/'
        response =requests.get(url)
        blog_detail = response.json()
        context={
            "blog_details":blog_detail
        }
        return render(request,'blogs/blog_details.html',context)

    def blog_categories(self,request):
        """
            List and Create categories
            
            Arguments:
                request (HttpRequest)
            
            Retunrns:
                In Get : list all categories 
                In Post : create new categories
        """
        return render(request,'blogs/categories.html')
    
    def myblog_view(self,request):
        """
            List blog of authenticated user
            
            Arguments:
                request (HttpRequest)
            
            Retunrns:
                In Get : list all blog for logged in user
        """
        if cache.get(f"access_token_{request.user.username}") :
            token = cache.get(f"access_token_{request.user.username}")
        else :
            token = refresh_token_for_user(request.user)
        return render(request,"blogs/myblogs.html",{"token" : token})

@login_required
def download_excel_data(request):
    """
        download blog report from cache  
        
        if not get in cache create celery task to generate and store report
    """
    if cache.get("is_report_generated"):
        return cache.get("blog_report")
    else:
        generate_blog_for_admin.apply_async()

        file_path = f"{settings.BASE_DIR}/reports/blog_reports.xlsx"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'attachment; filename="blog_report.xlsx"'
                cache.set("blog_report",response,timeout=60)
                return response
