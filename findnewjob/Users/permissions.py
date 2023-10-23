from rest_framework import permissions
from rest_framework.authtoken.models import Token


class ApplicantPermission(permissions.BasePermission):
    message = "У вас нет прав для выполнения этого действия"

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            if isinstance(request.auth, Token):
                if user.is_applicant:
                    return True
        return False


class EmployerPermission(permissions.BasePermission):
    message = "У вас нет прав для выполнения этого действия"

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            if isinstance(request.auth, Token):
                if user.is_employer:
                    return True
        return False
