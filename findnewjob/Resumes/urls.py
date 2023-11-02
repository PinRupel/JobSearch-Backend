from django.urls import path, include
from rest_framework import routers, viewsets
from .views import ResumeViewSet, GetResumeResponseAPIView, ResumeResponseAPIViewSet

app_name = 'Resume'

router = routers.DefaultRouter()
router.register(r'resume', ResumeViewSet)
router.register(r'response', ResumeResponseAPIViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('resume/<int:pk>/', include(router.urls)),
    path('resume/response/<int:pk>/', GetResumeResponseAPIView.as_view(), name='resume-response')
]
