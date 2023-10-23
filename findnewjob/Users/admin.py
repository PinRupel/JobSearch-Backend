from django.contrib import admin

from Users.models import User, Applicant, Employer

# Register your models here.
admin.site.register(User)
admin.site.register(Applicant)
admin.site.register(Employer)
