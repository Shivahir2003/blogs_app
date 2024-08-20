from django.core.cache import cache
from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


def generate_access_token(username,password):
    user_data = {"username": username,"password": password}

    jwt_token = TokenObtainPairSerializer(data =user_data)
    if jwt_token.is_valid():
        token = jwt_token.validated_data['access']
        cache.set(f"access_token_{username}",token,timeout=60)

def refresh_token_for_user(user):

    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
