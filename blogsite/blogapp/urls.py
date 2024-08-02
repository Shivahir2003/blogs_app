from django.urls import path

from blogapp.views import BlogAppView

app_name="blogapp"

urlpatterns = [
    path('',BlogAppView.as_view()),
    path('blog/dashboard',BlogAppView.as_view(), name="blog_dashboard"),
    path('blog/details/<int:pk>',BlogAppView.as_view(), name="blog_details"),
    path('blog/create',BlogAppView.as_view(), name="blog_create"),
    path('blog/edit/<int:pk>',BlogAppView.as_view(), name="blog_edit"),
    path('blog/delete/<int:pk>',BlogAppView.as_view(), name="blog_delete"),
    path('blog/category',BlogAppView.as_view(),name="blog_category")
]
