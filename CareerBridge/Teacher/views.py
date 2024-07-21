from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.hashers import check_password
from Admin import models


def TeacherLogin(request):
    TeacherPage = loader.get_template("TeacherLogin.html")
    HomePage = loader.get_template('home.html')
    if request.method == 'POST':
        FullName = request.POST.get('TeacherUserName')
        Password = request.POST.get('TeacherPassword')

        try:
            user = models.Teacher.objects.filter(FullName = FullName, Password = Password).first()
            if user:
                Image = models.Posters.objects.all()
                Class = models.TimeTable.objects.all()
                context = {
                    'Teacher' : FullName,
                    'image': Image,
                    'data' : {
                        'MobileNo': user.MobileNo,
                        'FullName': user.FullName
                    },
                    'Class' : Class
                }
                return HttpResponse(TeacherPage.render(context, request))
            else:
                context = {
                    'error': "Wrong"
                }
                return HttpResponse(HomePage.render(context, request))
        except Exception as e:
            context['error'] = f"Error: {str(e)}"
            return HttpResponse(HomePage.render(context, request))
        
def UpdateDetails(request):
    TeacherPage = loader.get_template('TeacherLogin.html')
    if request.method == 'POST': 
        FullName = request.POST.get('TeacherName')
        MobileNo = request.POST.get('TeacherMobileNo')
        UpdateMobileNo = request.POST.get('UpdateMobileNo')
        UpdatePassword = request.POST.get('UpdatePassword')
        
        try:
            user = models.Teacher.objects.filter(FullName = FullName, MobileNo = MobileNo).first()
            Image = models.Posters.objects.all()
            Class = models.TimeTable.objects.all()
            user.MobileNo = UpdateMobileNo
            user.Password = UpdatePassword
            user.save()
            context = {
                'success' : 'Successfully Updated',
                'Teacher' : FullName,
                    'image': Image,
                    'data' : {
                        'MobileNo': user.MobileNo,
                        'FullName': user.FullName,
                        'Password': user.Password
                    },
                    'Class' : Class
            }
            return HttpResponse(TeacherPage.render(context, request))
        
        except Exception as e:
            context['Success'] = f"Error: {str(e)}"
            return HttpResponse(TeacherPage.render(context,request))