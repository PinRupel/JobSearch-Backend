"""
URL configuration for findnewjob project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from Users.views import VerifyEmail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('activate/<uuid:activation_code>', VerifyEmail.as_view(), name='email-verify'),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/users/', include('Users.urls', namespace='Users')),
    path('api/', include('Resumes.urls', namespace='Resume')),
    path('api/', include('Vacancies.urls', namespace='Vacancies')),
]
