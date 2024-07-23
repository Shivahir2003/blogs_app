from django.urls import reverse
from django.shortcuts import render,redirect
from django.views.generic.base import View


class UserAuthenticationView(View):
    """ user authentication class """
    
    def dispatch(self,request,**kwargs):
        if request.path == reverse('accounts:user_login'):
            return self.login_view(request)
        elif request.path == reverse('accounts:user_logout'):
            return self.logout_view(request)
        elif request.path == reverse('accounts:user_signup'):
            return self.signup_view(request)
        elif request.path == reverse('accounts:user_list'):
            return self.show_all_user(request)
        else :
            return redirect('accounts:login')

    def login_view(self,request):
        return render(request,'accounts/login.html')

    def signup_view(self,request):
        return render(request,'accounts/signup.html')

    def logout_view(self,request):
        return redirect('accounts:user_login')

    def show_all_user(self,request):
        return render(request,'accounts/user_list.html')
    