from django.contrib import admin
from .models import CourseApplication, ProgramApplication
# Register your models here.
admin.site.register(CourseApplication)
admin.site.register(ProgramApplication)