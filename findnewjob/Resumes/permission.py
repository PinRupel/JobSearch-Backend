from rest_framework import permissions
from rest_framework.authtoken.models import Token


class ResumePermission(permissions.BasePermission):
    message = "У вас нет прав для создания резюме"

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'OPTIONS']:
            return True
        elif request.method in ['POST']:
            if request.user.is_authenticated:
                if isinstance(request.auth, Token):
                    if request.user.is_applicant:
                        return True
            return False
        elif request.method in ['DELETE', 'PUT', 'PATCH']:
            if request.user.is_authenticated:
                if isinstance(request.auth, Token):
                    if request.user.is_applicant:
                        if obj.user_id == request.user.id:
                            return True
            return False
        return False
