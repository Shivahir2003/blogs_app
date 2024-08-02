from django.urls import path,include

from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

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

app_name = "apiset"
urlpatterns = [
    path('', include(router_api.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
