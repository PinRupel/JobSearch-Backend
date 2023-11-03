from rest_framework import permissions
from rest_framework.authtoken.models import Token

from Vacancies.models import VacancyResponse


class VacancyPermission(permissions.BasePermission):
    message = "У вас нет прав для выполнения этого действия"

    def has_permission(self, request, view):
        if request.method in ['POST']:
            if request.user and request.user.is_authenticated:
                if isinstance(request.auth, Token):
                    if request.user.is_employer:
                        return True
            return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE', 'PUT', 'PATCH']:
            if request.user.is_authenticated:
                if isinstance(request.auth, Token):
                    if request.user.is_employer:
                        if obj.company_id == request.user.id:
                            return True
            return False
        else:
            return True


class ResponsePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            vacancy_id = view.kwargs.get('pk')
            if request.user.is_authenticated:
                if isinstance(request.auth, Token):
                    if request.user.is_applicant:
                        existing_response = VacancyResponse.objects.filter(applicant_id=request.user.id,
                                                                           vacancy_id=vacancy_id).exists()
                        if not existing_response:
                            return True
        else:
            response_id = int(view.kwargs.get('pk'))
            response_vacancy = VacancyResponse.objects.get(id=response_id)
            if response_vacancy.employer_id == request.user.id or response_vacancy.applicant_id == request.user.id:
                return True
        return False
