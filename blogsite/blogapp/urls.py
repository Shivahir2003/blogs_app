from django.urls import path

from blogapp.views import BlogAppView

app_name="blogapp"
urlpatterns = [
    path('blog/dashboard',BlogAppView.as_view(), name="blog_dashboard"),
    path('blog/details/<int:pk>',BlogAppView.as_view(), name="blog_details"),
    path('blog/create',BlogAppView.as_view(), name="blog_create"),
    path('blog/edit/<int:pk>',BlogAppView.as_view(), name="blog_edit"),
    path('blog/delete/<int:pk>',BlogAppView.as_view(), name="blog_delete"),
]
