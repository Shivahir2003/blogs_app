from django.urls import path

from accounts.views import indexview

urlpatterns = [
    path('list/',indexview,name='user_list'),
    path('user/signup',indexview,name='user_signup'),
    path('user/login',indexview,name='user_login'),
    path('user/logout',indexview,name='user_logout'),
    path('user/edit/<int:pk>',indexview,name='user_edit'),

]

# list/
# user/edit/<int:pk>
# user/login
# user/logout
# user/signup
