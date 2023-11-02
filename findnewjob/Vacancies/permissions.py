from rest_framework import permissions
from rest_framework.authtoken.models import Token


class VacancyPermission(permissions.BasePermission):
    message = "У вас нет прав для выполнения этого действия"

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'OPTIONS']:
            return True
        elif request.method in ['POST']:
            if request.user and request.user.is_authenticated:
                if isinstance(request.auth, Token):
                    if request.user.is_employer:
                        return True
            return False
        elif request.method in ['DELETE', 'PUT', 'PATCH']:
            if request.user.is_authenticated:
                if isinstance(request.auth, Token):
                    if request.user.is_employer:
                        if obj.name_company_id == request.user.id:
                            return True
            return False
        return False

# class VacancyPermission(permissions.BasePermission):
#     message = "У вас нет прав для выполнения этого действия"
#
#     def has_permission(self, request, view):
#         if request.method in ['POST']:
#             if request.user and request.user.is_authenticated:
#                 if isinstance(request.auth, Token):
#                     if request.user.is_employer:
#                         return True
#             return False
#         else:
#             return True
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in ['DELETE', 'PUT', 'PATCH']:
#             if request.user.is_authenticated:
#                 if isinstance(request.auth, Token):
#                     if request.user.is_employer:
#                         if obj.name_company_id == request.user.id:
#                             return True
#             return False
#         else:
#             return True