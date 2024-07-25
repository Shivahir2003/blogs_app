from django.urls import path,include

from rest_framework import routers

from apiset.views import (
    UserApi,
    BlogApi,
    Categorylist,
    CommentsList,
    ReplyList
    )

router_api = routers.DefaultRouter()
router_api.register(r'users',UserApi)
router_api.register(r'category',Categorylist)
router_api.register(r'blogs',BlogApi)
router_api.register(r'reply',ReplyList)
router_api.register(r'comments',CommentsList)

urlpatterns = [
    path('', include(router_api.urls)),
]
