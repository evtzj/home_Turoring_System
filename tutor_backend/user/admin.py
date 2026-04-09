from django.contrib import admin
from .models import User, TeacherProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'phone', 'role', 'is_verified', 'is_staff']
    search_fields = ['username', 'phone']
    list_filter = ['role', 'is_verified', 'is_staff']


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'subject', 'teaching_years', 'education']
    search_fields = ['user__username', 'subject']