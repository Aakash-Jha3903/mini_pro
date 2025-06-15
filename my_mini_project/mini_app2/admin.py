# admin.py
from django.contrib import admin
# from .models import Officials, OfficialsUser  # Updated import statement
from .models import  OfficialsUser  
from django.contrib.auth.admin import UserAdmin

from .models import  Student, SectionTeacher,TeacherRegistration # Updated import statement

@admin.register(OfficialsUser)
class OfficialsUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'password', 'created_at', 'updated_at']
    search_fields = ['name']
    ordering = ['name']  # Change this to the field you want to use for ordering


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'student_name','section']
    search_fields = ['student_id', 'student_name','section']
    ordering = ['student_id']  



@admin.register(SectionTeacher)
class SectionTeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher_id', 'password','section']
    search_fields = ['teacher_id','section']
    ordering = ['teacher_id']  

@admin.register(TeacherRegistration)
class TeacherRegistrationAdmin(admin.ModelAdmin):
    list_display = ['teacher_id', 'password','section']
    search_fields = ['teacher_id', 'section']
    ordering = ['teacher_id']  