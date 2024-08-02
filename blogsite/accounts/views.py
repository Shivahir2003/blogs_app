from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.contrib.auth.models import User


from accounts.forms import UserLoginForm


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
        """
            User login post method
            
            Arguments:
                request (HttpRequest)
            
            Required Parameters:
                username,password
            
            Retunrns:
                In Get:
                    render login.html page with empty login form
                In Post:
                    HttpResponseRedirect dashboard url if successful.
                    re-render page with error in validation error
        """
        if request.method == "GET":
            if request.user.is_authenticated:
                return redirect('blogapp:blog_dashboard')
            else:
                login_form=UserLoginForm()

        elif request.method =="POST":
            login_form=UserLoginForm(request.POST)
            if login_form.is_valid():
                username=login_form.cleaned_data['username']
                password=login_form.cleaned_data['password']

                # check if user is not exists redirect to signup view
                if not User.objects.filter(username=username).exists():
                    messages.error(request,'you have not signed up ')
                    return redirect('accounts:user_login')

                user = authenticate(request,username=username,password=password)
                if user is None:
                    messages.error(request,'invalid username or password')
                    return redirect('accounts:user_login')
                else:
                    login(request, user)
                    return redirect('blogapp:blog_dashboard')
        return render(request,'accounts/login.html',{'loginform':login_form})

    def signup_view(self,request):
        return render(request,'accounts/signup.html')

    @method_decorator(login_required)
    def logout_view(self,request):
        """
        User logout view
        
        Arguments:
            request (HttpRequest)
        
        Returns:
            render login.html page after logout successfull
        """
        logout(request)
        return redirect('accounts:user_login')

    def show_all_user(self,request):
        return render(request,'accounts/user_list.html')
    