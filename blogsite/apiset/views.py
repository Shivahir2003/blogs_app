from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView


from accounts.models import UserProfile
from blogapp.models import Blog,Category,Comments,Reply
from apiset.throttling import CommentsThrottlePerDay,CommentsThrottlePerSeconds
from apiset.serializers import (
    UserProfileSerializer,
    BlogSerializer,
    CategorySerializer,
    CommentSerializer,
    ReplySerializer,
    BlogListSerializer,
)


class UserApi(viewsets.ModelViewSet):

    queryset = UserProfile.objects.all()
    serializer_class= UserProfileSerializer

class BlogApi(viewsets.ModelViewSet):

    queryset = Blog.objects.select_related("user","categories").all()
    serializer_class =BlogSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'id']
    search_fields = ['title']
    ordering_fields = ['user', 'title','created']
    ordering = ['created']


    def get_seriablogslizer_class(self):
        """
            Return the correct serializer according to the action.
        """
        if self.action == "list":
            return BlogListSerializer
        else:
            return super().get_serializer_class()

class AuthBlogList(ListAPIView):
    serializer_class= BlogListSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post','delete']

    def get_queryset(self):
        queryset = Blog.objects.filter(user=self.request.user)
        return queryset


class Categorylist(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post','delete']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class CommentsList(viewsets.ModelViewSet):

    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    http_method_names=['get','post','patch','delete']
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes=[CommentsThrottlePerDay,CommentsThrottlePerSeconds]



class ReplyList(viewsets.ModelViewSet):

    queryset = Reply.objects.all()
    serializer_class =ReplySerializer
    http_method_names = ['get', 'post', 'patch','delete']
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
