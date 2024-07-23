from django.urls import path
from . import views

urlpatterns = [
    path("",views.test, name="test"),
    path('admin-login/', views.AdminLogin, name='admin_login'),
    path('student-registration/', views.StudentRegistration, name='student_registration'),
    path('TeacherRegistraion', views.TeacherRegistration, name='TeacherRegistration'),
    path('UploadImage', views.UploadImage, name='UploadImage'),
    path('ImageList', views.ImageList, name='ImageList'),
    path('TimeTable', views.TimeTable, name='TimeTable'),
    path('add_subject/', views.add_subject, name='add_subject'),
    path('delete_subject/', views.delete_subject, name='delete_subject'),
]