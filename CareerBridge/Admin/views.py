from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.hashers import check_password
from . import models
from django.contrib import messages
from Student import models as Smodels

def test(request):
    HomePage = loader.get_template("home.html")
    return render(request,"home.html")



def AdminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('AdminUserName')
        password = request.POST.get('AdminPassword')

        try:
            user = models.Admin.objects.filter(username=username, password = password).exists()
            TimeTable = models.TimeTable.objects.all()
            Subject = models.Subject.objects.all()
            Class = models.Class.objects.all()
            Students = models.Student.objects.all()
            FeeDetails = Smodels.FeeDetails.objects.all()
            if user:
                context = {
                    'error': "ADMIN",
                    'TimeTable' : TimeTable,
                    'Class' : Class,
                    'Subject' : Subject,
                    'FeeDetails': FeeDetails,
                    'Students' : Students
                }
                AdminPage = loader.get_template("AdminPage.html")
                return HttpResponse(AdminPage.render(context, request))
            else:
                context = {
                    'error': "Username or Password Wronggg"
                }
                HomePage = loader.get_template("home.html")
                return HttpResponse(HomePage.render(context, request))
        except models.Admin.DoesNotExist:
            context = {
                'error': "Username or Password Wrong11"
            }
            HomePage = loader.get_template("home.html")
            return HttpResponse(HomePage.render(context, request))

    return render(request, "home.html")

    
def StudentRegistration(request):
    AdminPage = loader.get_template("AdminPage.html")
    context = {}

    if request.method == 'POST':
        FullName = request.POST.get('SFullName')
        RollNo = request.POST.get('SRollNo')
        Class = request.POST.get('Class')

        if FullName == '' or RollNo == '' or Class == '':
            context = {
                'error' : "Enter Valid Details"
            }
            return HttpResponse(AdminPage.render(context,request))
        if models.Student.objects.filter(RollNo = RollNo):
            context = {
                'error' : "RollNo Already Exist"
            }
            return HttpResponse(AdminPage.render(context, request))

        try:
            data = models.Student(FullName = FullName, RollNo = RollNo, Password = RollNo, Class = Class)
            FeeDetails = Smodels.FeeDetails(StudentRollNo = RollNo, StudentName = FullName, Class = Class, TotalFee = 0, TotalPaidFee = 0, Due = 0, LatestPaidFee  = 0)
            data.save()
            FeeDetails.save()
            context['success'] = "Student Registered Successfully"
        except Exception as e:
            context['error'] = f"Error: {str(e)}"
            return HttpResponse(AdminPage.render(context, request))

    return HttpResponse(AdminPage.render(context, request))

def TeacherRegistration(request):
    AdminPage = loader.get_template("AdminPage.html")
    context = {}

    if request.method == 'POST':
        FullName = request.POST.get('TFullName')
        MobileNo = request.POST.get('TMobileNo')
        TeacherID = request.POST.get('TeacherID')
        ClassTeacher = request.POST.get('ClassTeacher')

        if models.Teacher.objects.filter(TeacherID = TeacherID):
            context = {
                'error' : "TeacherID Already Exists"
            }
            return HttpResponse(AdminPage.render(context, request))

        try:
            data = models.Teacher(FullName = FullName, MobileNo = MobileNo, Password = TeacherID, TeacherID = TeacherID, ClassTeacher = ClassTeacher)
            data.save()
            context['success'] = "Teacher Registered Successfully"
        except Exception as e:
            context['error'] = f"Error: {str(e)}"
            return HttpResponse(AdminPage.render(context, request))

    return HttpResponse(AdminPage.render(context, request))


        

        


def UploadImage(request):
    AdminPage = loader.get_template('AdminPage.html')
    if request.method == 'POST':
        Title = request.POST.get('Title')
        Description = request.POST.get('Description')
        Image = request.FILES.get('Image')
        data = models.Posters.objects.create(Title = Title, Description = Description, Image=Image)
        data.save()
        context = {
            'success':"Successfully Uploaded Updates"
        }
        return HttpResponse(AdminPage.render(context, request))
    return render(request, 'AdminPage.html')

def ImageList(request):
    image = models.Posters.objects.all()
    return render(request, 'StudentLogin.html', {'image': image})



def TimeTable(request):
    AdminPage = loader.get_template('AdminPage.html')
    Data = models.TimeTable.objects.all().values()
    
    if request.method == 'POST':
        Class = request.POST.get('Class')
        TimeTable = request.FILES.get('TimeTable')

        ClassExist = models.TimeTable.objects.filter(Class=Class)
        if not ClassExist.exists():
            data = models.TimeTable.objects.create(Class=Class, Image=TimeTable)
            data.save()
        else:
            data = models.TimeTable.objects.get(Class=Class)
            data.Image = TimeTable
            data.save()
            
        context = {
            'success': 'Successfully Uploaded Timetables',
            'TimeTable': models.TimeTable.objects.all()
        }
        
        return HttpResponse(AdminPage.render(context, request))
    
    context = {
        'TimeTable': models.TimeTable.objects.all().values()
    }
    
    return HttpResponse(AdminPage.render(context, request))



def add_subject(request):
    AdminPage = loader.get_template('AdminPage.html')
    TimeTable = models.TimeTable.objects.all()
    Subject = models.Subject.objects.all()
    Class = models.Class.objects.all()
    if request.method == 'POST':
        class_name = request.POST['Class']
        sub_code = request.POST['SubCode']
        subject_name = request.POST['Subject']

        if models.Subject.objects.filter(Class = class_name, SubCode = sub_code).first() or models.Subject.objects.filter(Class = class_name, Subject = subject_name):
            context = {
                'error' : "Subject already exists",
                'Admin': "ADMIN",
                'TimeTable' : TimeTable,
                'Class' : Class,
                'Subject' : Subject
            }
            return HttpResponse(AdminPage.render(context, request))


        # Create and save the new subject
        new_subject = models.Subject(Class=class_name, SubCode=sub_code, Subject=subject_name)
        new_subject.save()
        

        messages.success(request, 'Subject added successfully')
        context = {
            'success' : "Subject added successfully",
            'error': "ADMIN",
            'TimeTable' : TimeTable,
            'Class' : Class,
            'Subject' : Subject

        }
        return HttpResponse(AdminPage.render(context,request))

def delete_subject(request):
    AdminPage = loader.get_template('AdminPage.html')
    if request.method == 'POST':
        subject_id = request.POST['subject_id']

        # Delete the subject
        models.Subject.objects.filter(id=subject_id).delete()
        TimeTable = models.TimeTable.objects.all()
        Subject = models.Subject.objects.all()
        Class = models.Class.objects.all()

        context = {
            'success' : "Subject deleted successfully",
            'error': "ADMIN",
            'TimeTable' : TimeTable,
            'Class' : Class,
            'Subject' : Subject
        }
        return HttpResponse(AdminPage.render(context,request))
    
def UpdateFeeDetails(request):
    AdminPage = loader.get_template("AdminPage.html")
    context = {}

    if request.method == 'POST':
        StudentRollNo = request.POST.get('StudentRollNo')
        StudentName = request.POST.get('StudentName')
        Class = request.POST.get('Class')
        TotalFee = request.POST.get('TotalFee')
        LatestPaidFee = request.POST.get('LatestPaidFee')
        TotalPaidFee = request.POST.get('TotalPaidFee')

        StudentExist = Smodels.FeeDetails.objects.filter(StudentRollNo = StudentRollNo, StudentName = StudentName, Class = Class).first()
        TimeTable = models.TimeTable.objects.all()
        Subject = models.Subject.objects.all()
        Class = models.Class.objects.all()
        Students = models.Student.objects.all()
        FeeDetails = Smodels.FeeDetails.objects.all()

        try:
            if StudentExist:
                StudentExist.TotalFee = TotalFee
                StudentExist.LatestPaidFee = LatestPaidFee
                StudentExist.TotalPaidFee = float(StudentExist.TotalPaidFee) + float(LatestPaidFee)
                StudentExist.Due = float(StudentExist.TotalFee) - float(StudentExist.TotalPaidFee)

                StudentExist.save()

                context = {
                    'success' : "Fee updated successfully",
                    'TimeTable' : TimeTable,
                    'Class' : Class,
                    'Subject' : Subject,
                    'FeeDetails': FeeDetails,
                    'Students' : Students

                }
                return HttpResponse(AdminPage.render(context, request))
            else:
                context = {
                    'error' : "Fee updation failed",
                    'TimeTable' : TimeTable,
                    'Class' : Class,
                    'Subject' : Subject,
                    'FeeDetails': FeeDetails,
                    'Students' : Students
                } 
                return HttpResponse(AdminPage.render(context, request))
        except Exception as e:
            context['error'] = f"Error: {str(e)}"
            return HttpResponse(AdminPage.render(context, request))
    context = {
        'error' : "Error"
    }
    return HttpResponse(AdminPage.render(context,request))

