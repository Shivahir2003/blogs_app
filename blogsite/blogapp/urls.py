from django.urls import path

from blogapp.views import indexview

urlpatterns = [
    path('blog/dashboard',indexview, name="blog_dashboard"),
    path('blog/create',indexview, name="blog_create"),
    path('blog/edit/<int:pk>',indexview, name="blog_edit"),
    path('blog/delete/<int:pk>',indexview, name="blog_delete"),
]

# blogs/ ...

# blog/dashboard
# blog/list/all
# blog/create
# blog/edit/<int:pk>
# blog/delete/<int:pk>
# blog//<int:pk>
