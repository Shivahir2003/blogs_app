from rest_framework.permissions import BasePermission

class UserDetailWritePermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if request.method =="GET" and request.parser_context['kwargs']:
            if not user.is_authenticated:
                return False
        return True
        