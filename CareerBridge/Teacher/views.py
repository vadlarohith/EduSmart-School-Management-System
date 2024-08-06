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
                Image = models.Posters.objects.all().values()
                TimeTable = models.TimeTable.objects.all()
                Student = models.Student.objects.filter(Class = user.ClassTeacher)
                context = {
                    'Teacher' : FullName,
                    'images': Image,
                    'data' : {
                        'MobileNo': user.MobileNo,
                        'FullName': user.FullName
                    },
                    'TimeTable' : TimeTable,
                    'Student' : Student
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
            TimeTable = models.TimeTable.objects.all()
            Student = models.Student.objects.filter(Class = user.ClassTeacher)
            user.MobileNo = UpdateMobileNo
            user.Password = UpdatePassword
            user.save()
            context = {
                'success' : 'Successfully Updated',
                'Teacher' : FullName,
                    'images': Image,
                    'data' : {
                        'MobileNo': user.MobileNo,
                        'FullName': user.FullName,
                        'Password': user.Password
                    },
                    'Class' : Class,
                    'TimeTable' : TimeTable,
                    'Student' : Student
            }
            return HttpResponse(TeacherPage.render(context, request))
        
        except Exception as e:
            context['Success'] = f"Error: {str(e)}"
            return HttpResponse(TeacherPage.render(context,request))
        
def Attendence1(request):
    TeacherPage = loader.get_template('TeacherLogin.html')
    if request.method == 'POST':
        FullName = request.POST.get('TeacherName')
        MobileNo = request.POST.get('TeacherMobileNo')
        user = models.Teacher.objects.filter(FullName = FullName, MobileNo = MobileNo).first()
        Image = models.Posters.objects.all()
        Class = models.TimeTable.objects.all()
        TimeTable = models.TimeTable.objects.all()
        Student = models.Student.objects.filter(Class = user.ClassTeacher)
    context = {
        'Teacher' : FullName,
        'images' : Image,
        'data' : {
                'MobileNo': user.MobileNo,
                'FullName': user.FullName,
                'Password': user.Password
            },
        'Class' : Class,
        'TimeTable' : TimeTable,
        'Student' : Student
    }
    if request.method == 'POST':
        num_student = len(request.POST) // 3

        for i in range(1,num_student+2):
            SRegNo = request.POST.get(f'SRegNo_{i}')
            Month = request.POST.get(f'Month_{i}')
            Attendence = 'P' if request.POST.get(f'Attendence_{i}') == 'on' else 'A'
            AttendenceDate = request.POST.get('AttendenceDate')

            context['Attendence'] = Attendence
            if Attendence == "":
                continue

            try:
                """user = models.Attendence.objects.filter(RegNo = SRegNo, Month = Month).first()
                if user:
                    user.RegNo = SRegNo
                    user.Month = Month
                    user.Attendence = Attendence
                    user.save()
                else:
                    data = models.Attendence(RegNo = SRegNo, Month = Month, Attendence = Attendence)
                    data.save()"""
                AttendenceDetailsExists = models.AttendenceDetails.objects.filter(RegNo = SRegNo, AttendenceDate = AttendenceDate).first()
                if AttendenceDetailsExists:
                    AttendenceDetailsExists.RegNo = SRegNo
                    AttendenceDetailsExists.Attendence = Attendence
                    AttendenceDetailsExists.AttendenceDate = AttendenceDate
                    AttendenceDetailsExists.save()
                else:
                    data1 = models.AttendenceDetails(RegNo = SRegNo, Attendence = Attendence, AttendenceDate = AttendenceDate)
                    data1.save()

            except Exception as e:
                context['error'] = f"Error saving data for student {SRegNo}: {str(e)}"
                return HttpResponse(TeacherPage.render(context, request))
            
        context['success'] = "Attendance Successfully Updated"
        return HttpResponse(TeacherPage.render(context, request))
    context['error'] = "Invalid Request Method"
    return HttpResponse(TeacherPage.render(context, request))