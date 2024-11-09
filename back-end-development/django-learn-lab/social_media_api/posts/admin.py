from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, Comment

admin.site.register(Post)
admin.site.register(Comment)