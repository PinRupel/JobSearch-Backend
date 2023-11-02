from rest_framework import permissions
from rest_framework.authtoken.models import Token

from Vacancies.models import VacancyResponse


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


class ResponsePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if obj.employer_id == request.user.id or obj.applicant_id == request.user.id:
                return True
        return False

    def has_permission(self, request, view):
        vacancy_id = view.kwargs.get('pk')
        if request.method == 'POST':
            if request.user.is_authenticated:
                if isinstance(request.auth, Token):
                    if request.user.is_applicant:
                        existing_response = VacancyResponse.objects.filter(applicant_id=request.user.id,
                                                                           vacancy_id=vacancy_id).exists()
                        if not existing_response:
                            return True
        return False
