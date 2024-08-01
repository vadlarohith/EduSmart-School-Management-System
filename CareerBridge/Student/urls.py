from django.urls import path
from . import views

urlpatterns = [
    path('student-login',views.StudentLogin, name="student-login"),
    path('UpdateStudentDetails', views.UpdateDetails, name="UpdateStudentDetails"),
    path('Attendence', views.Attendence, name='Attendence'),
    
]
