from django.core.cache import cache

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


def generate_access_token(username,password):
    user_data = {"username": username,"password": password}

    if cache.get(f"access_token_{username}"):
        print("from cache memory")
        print(cache.ttl(f"access_token_{username}"))
        token = cache.get(f"access_token_{username}")
    else :
        jwt_token = TokenObtainPairSerializer(data =user_data)
        if jwt_token.is_valid():
            print("from data base")
            token = jwt_token.validated_data['access']
            cache.set(f"access_token_{username}",token,timeout=60)
    return token

