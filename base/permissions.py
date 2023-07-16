from rest_framework import permissions


class ApiKeyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # el api key se podria definir en el .env o en el settings para que quede mejor
        return request.headers.get('x-api-key') == "api_key"