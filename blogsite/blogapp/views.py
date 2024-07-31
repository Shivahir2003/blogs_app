import requests
from django.urls import reverse
from django.shortcuts import render
from django.views.generic.base import View


from blogapp.forms import BlogForm
from blogapp.models import Blog



class BlogAppView(View):
    """ Blog application views """
    
    def dispatch(self,request,**kwargs):
        if request.path == reverse("blogapp:blog_create"):
            return self.blog_add(request)
        elif request.path == reverse("blogapp:blog_dashboard"):
            return self.dashboard(request)
        elif request.path == reverse("blogapp:blog_category"):
            return self.blog_categories(request)
        elif '/blogs/blog/details/'in request.path:
            return self.blog_details(request,**kwargs)
        elif '/blogs/blog/edit/'in request.path:
            return self.blog_edit(request,**kwargs)

    def dashboard(self,request):
        return render(request,'blogs/dashboard.html')

    def blog_add(self,request):
        form = BlogForm()
        context = {
            "form": form
        }
        return render(request,'blogs/add_blog.html' ,context)

    def blog_edit(self,request,pk):
        blog=Blog.objects.get(pk=pk)
        form = BlogForm(instance=blog)
        context = {
            "form": form,
            "pk": pk
        }
        return render(request,'blogs/edit_blog.html' ,context)
    
    def blog_details(self,request,pk):
        url= f'http://127.0.0.1:8000/api/blogs/{pk}/'
        response =requests.get(url)
        blog_detail = response.json()
        context={
            "blog_details":blog_detail
        }
        return render(request,'blogs/blog_details.html',context)
    
    def blog_categories(self,request):
        return render(request,'blogs/categories.html')
