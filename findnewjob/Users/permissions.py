from rest_framework import permissions


class ApplicantPermission(permissions.BasePermission):
    message = "У вас нет прав для выполнения этого действия"

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.is_applicant:
            return True
        return False


class EmployerPermission(permissions.BasePermission):
    message = "У вас нет прав для выполнения этого действия"

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.is_employer:
            return True
        return False
