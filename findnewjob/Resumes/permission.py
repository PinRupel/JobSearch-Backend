from rest_framework import permissions
from rest_framework.authtoken.models import Token

from Resumes.models import ResumeResponse


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


class ResumeResponsePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            resume = view.kwargs.get('pk')
            if request.user.is_authenticated:
                if isinstance(request.auth, Token):
                    if request.user.is_employer:
                        existing_response = ResumeResponse.objects.filter(employer=request.user.id,
                                                                          resume=resume).exists()
                        if not existing_response:
                            return True
        else:
            response_id = int(view.kwargs.get('pk'))
            response_resume = ResumeResponse.objects.get(id=response_id)
            if response_resume.employer_id == request.user.id or response_resume.applicant_id == request.user.id:
                return True
        return False