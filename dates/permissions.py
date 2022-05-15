from rest_framework.permissions import BasePermission


class CheckApiKeyAuth(BasePermission):
    """
        It is just to check weather or not the client deliver the api-key in the request header
    """
    def has_permission(self, request, view):
        api_key_secret = request.META.get("HTTP_X_API_KEY")
        if api_key_secret: return True
