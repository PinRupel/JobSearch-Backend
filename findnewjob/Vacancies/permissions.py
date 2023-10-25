from rest_framework import permissions
from rest_framework.authtoken.models import Token


class EmployerPermission(permissions.BasePermission):
    message = "У вас нет прав для выполнения этого действия"

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated:
            if isinstance(request.auth, Token):
                if user.is_employer:
                    return True
        return False


class EmployerUpdatePermissions(permissions.BasePermission):
    message = "У вас нет прав для изменения данных в вакансии"

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if isinstance(request.auth, Token):
                if request.user.is_employer:
                    if obj.name_company_id == request.user.id:
                        return True
        return False


class EmployerDeletePermissions(permissions.BasePermission):
    message = "У вас нет прав для удаления данной вакансии"

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if isinstance(request.auth, Token):
                if request.user.is_employer:
                    if obj.name_company_id == request.user.id:
                        return True
        return False
