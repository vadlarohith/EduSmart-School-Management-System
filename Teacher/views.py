from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.hashers import check_password
from Admin import models
from django.db.models import Func, F
from django.http import JsonResponse

def TeacherLogin(request):
    TeacherPage = loader.get_template("TeacherLogin1.html")
    HomePage = loader.get_template('home.html')
    if request.method == 'POST':
        FullName = request.POST.get('TeacherUserName')
        Password = request.POST.get('TeacherPassword')
        

        try:
            user = models.Teacher.objects.filter(FullName = FullName, Password = Password).first()
            if user:
                Image = models.Posters.objects.all().values()[::-1]
                TimeTable = models.TimeTable.objects.all()
                Student = models.Student.objects.filter(Class = user.ClassTeacher)
                ExamMarks1 = models.ExamMarks.objects.filter(Subject = user.Subject).all()
                context = {
                    'Teacher' : FullName,
                    'images': Image,
                    'data' : {
                        'MobileNo': user.MobileNo,
                        'FullName': user.FullName,
                        'TeacherID' : user.TeacherID,
                        'Profile' : user.Profile
                    },
                    'TimeTable' : TimeTable,
                    'Student' : Student,
                    'ExamMarks' : models.ExamMarks.objects.filter(Subject__iexact = user.Subject).all(), #__iexact is for CASE-INCENSITIVE
                    'Access' : models.ExamType.objects.all(),
                    'TeacherTimetable' : models.TeacherTimetable.objects.filter(TeacherID = user.TeacherID).first()
                }
                return HttpResponse(TeacherPage.render(context, request))
            else:
                context = {
                    'error' : "Username or Password is incorrect. Please enter correct valid details."
                }
                return HttpResponse(HomePage.render(context, request))
        except Exception as e:
            context['error'] = f"Error: {str(e)}"
            return HttpResponse(HomePage.render(context, request))
        
def UpdateDetails(request):
    TeacherPage = loader.get_template('TeacherLogin1.html')
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
                    'Password': user.Password,
                    'TeacherID' : user.TeacherID,
                    'Profile' : user.Profile
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
    TeacherPage = loader.get_template('TeacherLogin1.html')
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
        'images' : Image[::-1],
        'data' : {
                'MobileNo': user.MobileNo,
                'FullName': user.FullName,
                'Password': user.Password,
                'TeacherID' : user.TeacherID,
                'Profile' : user.Profile
            },
        'Class' : Class,
        'TimeTable' : TimeTable,
        'Student' : Student,
        'Attendence' : models.AttendenceDetails.objects.all(),
        'ExamMarks' : models.ExamMarks.objects.filter(Subject__iexact = user.Subject).all(), #__iexact is for CASE-INCENSITIVE
        'Access' : models.ExamType.objects.all()
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
            return HttpResponse(TeacherPage.render(context, request))
        context['success'] = "Attendance Successfully Updated"
        return HttpResponse(TeacherPage.render(context, request))
    return HttpResponse(TeacherPage.render(context, request))


def ExamMarks(request):
    TeacherPage = loader.get_template('TeacherLogin1.html')
    if request.method == 'POST':
        FullName = request.POST.get('TeacherName')
        MobileNo = request.POST.get('TeacherMobileNo')
        user = models.Teacher.objects.filter(FullName = FullName, MobileNo = MobileNo).first()
        context = {
        'Teacher' : FullName,
        'images': models.Posters.objects.all(),
        'data' : {
            'MobileNo': user.MobileNo,
            'FullName': user.FullName,
            'TeacherID' : user.TeacherID,
            'Profile' : user.Profile
        },
        'TimeTable' : models.TimeTable.objects.all(),
        'Student' : models.Student.objects.filter(Class = user.ClassTeacher),
        'ExamMarks' : models.ExamMarks.objects.filter(Subject__iexact = user.Subject).all(),
    }
    
    if request.method == 'POST':
        num_students = len([key for key in request.POST.keys() if key.startswith('StudentRollNo_')])
        for i in range(1,num_students+1):
            SRollNo = request.POST.get(f'StudentRollNo_{i}')
            SName = request.POST.get(f'StudentName_{i}')
            Subject = request.POST.get('Subject')
            Class = request.POST.get('Class')
            ExamType = request.POST.get('ExamType')
            Marks = request.POST.get(f'Marks_{i}')

            context['Access'] = models.ExamType.objects.all()
            if int(Marks) > models.ExamType.objects.filter(ExamType = ExamType).first().MaxMarks:
                context['error'] = 'Enter valid marks'
                return HttpResponse(TeacherPage.render(context, request))

            try:
                StudentExists = models.ExamMarks.objects.filter(StudentRollNo = SRollNo, StudentName = SName, Subject = Subject,ExamType = ExamType).first()
                if StudentExists:
                    StudentExists.Marks = int(Marks)
                    StudentExists.save()
                else:
                    StudentMarksData = models.ExamMarks(StudentRollNo = SRollNo, StudentName = SName, Subject = Subject, Class = Class, ExamType = ExamType, Marks = Marks)
                    StudentMarksData.save()
            except Exception as e:
                context['error'] = f"Error saving data for student {SRollNo}: {str(e)}"
                return HttpResponse(TeacherPage.render(context, request))
        context['success'] = "Attendance Successfully Updated"
        return HttpResponse(TeacherPage.render(context, request))
    context['error'] = "Invalid Request Method"
    return HttpResponse(TeacherPage.render(context, request))

def ProfileUpdate1(request):
    TeacherPage = loader.get_template('TeacherLogin1.html')
    if request.method == 'POST':
        FullName = request.POST.get('FullName')
        TeacherID = request.POST.get('TeacherID')
        Profile = request.FILES.get('profileImage')
        user = models.Teacher.objects.filter(FullName = FullName, TeacherID = TeacherID).first()
        Image = models.Posters.objects.all().values()[::-1]
        TimeTable = models.TimeTable.objects.all()
        Student = models.Student.objects.filter(Class = user.ClassTeacher)
        ExamMarks1 = models.ExamMarks.objects.filter(Subject = user.Subject).all()
        context = {
            'Teacher' : FullName,
            'images': Image,
            'data' : {
                'MobileNo': user.MobileNo,
                'FullName': user.FullName,
                'TeacherID' : user.TeacherID,
                'Profile' : user.Profile
            },
            'TimeTable' : TimeTable,
            'Student' : Student,
            'ExamMarks' : models.ExamMarks.objects.filter(Subject__iexact = user.Subject).all(), #__iexact is for CASE-INCENSITIVE
            'Access' : models.ExamType.objects.all()
        }

        try:
            user.Profile = Profile
            user.save()
        except Exception as e:
            context['Success'] = f"Error: {str(e)}"

        return HttpResponse(TeacherPage.render(context, request))
    return HttpResponse(TeacherPage.render(context, request))

