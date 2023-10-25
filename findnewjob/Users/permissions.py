from rest_framework import permissions
from rest_framework.authtoken.models import Token


class IsCurApplicantOrReadOnly(permissions.BasePermission):
    message = "У вас нет прав для выполнения этого действия"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if user and user.is_authenticated:
            if isinstance(request.auth, Token):
                return user.is_applicant and str(user.id) == view.kwargs.get('pk')
        return False


class IsCurEmployerOrReadOnly(permissions.BasePermission):
    message = "У вас нет прав для выполнения этого действия"

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if user and user.is_authenticated:
            if isinstance(request.auth, Token):
                return user.is_employer and str(user.id) == view.kwargs.get('pk')
        return False
