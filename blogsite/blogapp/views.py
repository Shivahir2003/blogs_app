from django.urls import reverse
from django.shortcuts import render,redirect
from django.views.generic.base import View


class BlogAppView(View):
    """ Blog application views """
    
    def dispatch(self,request,**kwargs):
        if request.path == reverse("blogapp:blog_create"):
            return self.add_blog(request)
        elif request.path == reverse("blogapp:blog_dashboard"):
            return self.dashboard(request)
        elif request.path == reverse("blogapp:blog_details"):
            return self.blog_details(request)

    def dashboard(self,request):
        return render(request,'blogs/dashboard.html')

    def add_blog(self,request):
        return render(request,'blogs/add_edit_blog.html')

    def blog_details(self,request):
        return render(request,'blogs/blog_details.html')
