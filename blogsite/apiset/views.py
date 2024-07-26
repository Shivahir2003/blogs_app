from django.contrib.auth.models import User

from rest_framework import viewsets

from blogapp.models import Blog,Category,Comments,Reply
from apiset.serializers import (
    UserSerializer,
    BlogSerializer,
    CategorySerializer,
    CommentSerializer,
    ReplySerializer,
    BlogListSerializer,
)


class UserApi(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class= UserSerializer

class BlogApi(viewsets.ModelViewSet):

    queryset = Blog.objects.all()
    serializer_class =BlogSerializer

    def get_serializer_class(self):
        """
            Return the correct serializer according to the action.
        """
        if self.action == "list":
            return BlogListSerializer
        else:
            return super().get_serializer_class()


class Categorylist(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post','delete']


class CommentsList(viewsets.ModelViewSet):

    queryset = Comments.objects.all()
    serializer_class = CommentSerializer


class ReplyList(viewsets.ModelViewSet):

    queryset = Reply.objects.all()
    serializer_class =ReplySerializer
    http_method_names = ['get', 'post', 'patch','delete']
