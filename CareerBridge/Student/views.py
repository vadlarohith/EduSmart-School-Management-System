"""from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.hashers import check_password
from Admin import models

def StudentLogin(request):
    StudentPage = loader.get_template("StudentLogin.html")
    HomePage = loader.get_template("home.html")
    Data = models.Student.objects.all().values()
    if request.method == 'POST':
        FullName = request.POST.get('StudentUserName')
        Password = request.POST.get('StudentPassword')

        try:
            user = models.Student.objects.filter(FullName = FullName, Password = Password).first()
            if user:
                image = models.Posters.objects.all()
                data = models.Student.objects.all()
                Class = user.Class
                TimeTable = models.TimeTable.objects.filter(Class = Class).exists()
                context = {
                    'Student': FullName,
                    'image' : image,
                    'data' : {
                        'FullName': user.FullName,
                        'RollNo' : user.RollNo,
                        'MobileNo': user.MobileNo,
                        'Password': user.Password,
                        'Class' : user.Class
                    },
                    'TimeTable': TimeTable
                }
                return HttpResponse(StudentPage.render(context, request))
            else:
                context = {
                    'error' : "Wrong"
                }
                return HttpResponse(HomePage.render(context, request))
            
        except Exception as e:
            context['error'] = f"Error: {str(e)}"
            return HttpResponse(HomePage.render(context, request))
        
def UpdateDetails(request):
    StudentPage = loader.get_template('StudentLogin.html')
    if request.method == 'POST': 
        FullName = request.POST.get('StudentName')
        RollNo = request.POST.get('StudentRollNo')
        UpdateMobileNo = request.POST.get('UpdateMobileNo')
        UpdatePassword = request.POST.get('UpdatePassword')
        
        try:
            user = models.Student.objects.filter(FullName = FullName, RollNo = RollNo).first()
            user.MobileNo = UpdateMobileNo
            user.Password = UpdatePassword
            user.save()
            context = {
                'success' : 'Successfully Updated'
            }
            return HttpResponse(StudentPage.render(context, request))
        
        except Exception as e:
            context['Success'] = f"Error: {str(e)}"
            return HttpResponse(StudentPage.render(context,request))"""
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.hashers import check_password
from Admin import models

def StudentLogin(request):
    StudentPage = loader.get_template("StudentLogin.html")
    HomePage = loader.get_template("home.html")
    if request.method == 'POST':
        FullName = request.POST.get('StudentUserName')
        Password = request.POST.get('StudentPassword')

        try:
            user = models.Student.objects.filter(FullName=FullName, Password=Password).first()
            if user:
                image = models.Posters.objects.all()
                Class = user.Class
                TimeTable = models.TimeTable.objects.filter(Class=Class).first()

                # Debugging output
                if TimeTable:
                    print(f"TimeTable: {TimeTable}")
                    print(f"TimeTable Image: {TimeTable.Image}")
                context = {
                    'Student': FullName,
                    'image': image,
                    'data': {
                        'FullName': user.FullName,
                        'RollNo': user.RollNo,
                        'MobileNo': user.MobileNo,
                        'Password': user.Password,
                        'Class': user.Class
                    },
                    'TimeTable': TimeTable
                }
                return HttpResponse(StudentPage.render(context, request))
            else:
                context = {
                    'error': "Wrong"
                }
                return HttpResponse(HomePage.render(context, request))
        except Exception as e:
            context = {
                'error': f"Error: {str(e)}"
            }
            return HttpResponse(HomePage.render(context, request))

def UpdateDetails(request):
    StudentPage = loader.get_template('StudentLogin.html')
    if request.method == 'POST':
        FullName = request.POST.get('StudentName')
        RollNo = request.POST.get('StudentRollNo')
        UpdateMobileNo = request.POST.get('UpdateMobileNo')
        UpdatePassword = request.POST.get('UpdatePassword')

        try:
            user = models.Student.objects.filter(FullName=FullName, RollNo=RollNo).first()
            user.MobileNo = UpdateMobileNo
            user.Password = UpdatePassword
            user.save()
            context = {
                'success': 'Successfully Updated'
            }
            return HttpResponse(StudentPage.render(context, request))
        except Exception as e:
            context = {
                'success': f"Error: {str(e)}"
            }
            return HttpResponse(StudentPage.render(context, request))
