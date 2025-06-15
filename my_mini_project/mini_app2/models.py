# mini_app2/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import ASCIIUsernameValidator

class OfficialsManager(BaseUserManager):
    def create_user(self, name, password=None, **extra_fields):
        if not name:
            raise ValueError('The Name field must be set')
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(name, password, **extra_fields)

class OfficialsUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=30, unique=True, validators=[ASCIIUsernameValidator()])
    password = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = OfficialsManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []  # Add other fields if needed

    def __str__(self):
        return self.name
    
class Student(models.Model):
    student_id = models.BigIntegerField(unique=True)
    student_name = models.CharField(max_length=50)
    student_aadhar = models.BigIntegerField(unique=True)
    student_phone = models.CharField(max_length=20)
    student_email = models.EmailField()
    
    gender = models.CharField(max_length=10, choices=[("male", "Male"), ("female", "Female")])
    student_dob = models.DateField()
    student_address = models.TextField()

    father_name = models.CharField(max_length=50)  
    father_phone = models.CharField(max_length=20)
    mother_name = models.CharField(max_length=50)
    mother_phone = models.CharField(max_length=20)

    school_name = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    state_name = models.CharField(max_length=50)
    city_name = models.CharField(max_length=50)
    
    attendance = models.PositiveIntegerField(default=0)
    marks = models.PositiveIntegerField()
    fees = models.CharField(max_length=10, default='Unpaid')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.student_name} ({self.student_id}) - {self.section}"


class SectionTeacher(models.Model):
    teacher_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    section = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.teacher_id} -- {self.section}"


class TeacherRegistration(models.Model):
    teacher_id = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=200)
    section = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.teacher_id} -- {self.section}"
