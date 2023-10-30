from django.urls import path, include
from rest_framework import routers
from .views import ResumeViewSet

app_name = 'Resumes'

router = routers.DefaultRouter()
router.register(r'resumes', ResumeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
