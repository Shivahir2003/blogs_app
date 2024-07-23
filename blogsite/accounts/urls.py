from django.urls import path

from accounts.views import UserAuthenticationView

app_name="accounts"
urlpatterns = [
    path('list/',UserAuthenticationView.as_view(),name='user_list'),
    path('user/signup',UserAuthenticationView.as_view(),name='user_signup'),
    path('user/login',UserAuthenticationView.as_view(),name='user_login'),
    path('user/logout',UserAuthenticationView.as_view(),name='user_logout'),

]
