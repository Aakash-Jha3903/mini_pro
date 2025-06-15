"""
URL configuration for my_mini_project project.

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
from django.conf import settings  # for static files at deploy time
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views
from mini_app2 import views
# from django.contrib.auth.views import LogoutView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # path('officials/', views.officials, name='officials'),
    path('officials/', views.Officials, name='officials'),
    path('logout_officials/', views.logout_officials, name='logout_officials'),
    path('ST_login/', views.ST_login, name='ST_login'),
    path('services/', views.services, name='services'),

    path('teacher_registration/', views.teacher_registration, name='teacher_registration'),
    path('teacher_login/', views.teacher_login, name='teacher_login'),
    path('teacher_dashboard/<str:section>/', views.teacher_dashboard, name='teacher_dashboard'),

    path('contact/', views.contact, name='contact'),
    path('data_analysis/', views.data_analysis, name='data_analysis'),
    path('export_excel/', views.export_excel, name='export_excel'),
    
    path('search/', views.search, name='search'),
    path('download_csv/', views.download_csv, name='download_csv'),
    path('email_download_csv/', views.email_download_csv, name='email_download_csv'),  
    
    # path('download_excel/', views.download_excel, name='download_excel'),
    path('delete_selected/', views.delete_selected, name='delete_selected'),
    path('update_student/<int:student_id>/',views.update_student, name='update_student'),
    
    path('data_visualization/', views.data_visualization,name='data_visualization'),
    
    path('form/', views.form, name='form'),
    path('student_login/', views.student_login, name='student_login'),
    path('student_details/<int:student_id>/', views.student_details, name='student_details'),
    
    path('otp_verification/', views.otp_verification, name='otp_verification'),
    # path('otp_verification/<str:student_email>/', views.otp_verification, name='otp_verification'),
    path('thanks/', views.thanks, name='thanks'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
