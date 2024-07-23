from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.hashers import check_password
from . import models

def test(request):
    HomePage = loader.get_template("home.html")
    return render(request,"home.html")

"""def AdminLogin(request):
    admin = models.admin.objects.all().values()
    AdminPage = loader.get_template("AdminPage.html")
    HomePage = loader.get_template("home.html")
    if request.method == 'POST':
        username = request.POST['AdminUserName']
        password = request.POST['AdminPassword']

        user = models.admin.objects.filter(Username=username,Password=password).first()
        if user:
            context = {
                'error' : "ADMIN"
            }
            return HttpResponse(AdminPage.render(context,request))
        context = {
            'error' : "Username or Password Wrong"
        }
        return HttpResponse(HomePage.render(context,request))
    return render(request, "home.html")"""

def AdminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('AdminUserName')
        password = request.POST.get('AdminPassword')

        try:
            user = models.Admin.objects.filter(username=username, password = password).exists()
            TimeTable = models.TimeTable.objects.all()
            if user:
                context = {
                    'error': "ADMIN",
                    'TimeTable' : TimeTable
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
            data.save()
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


"""def TimeTable(request):
    AdminPage = loader.get_template('AdminPage.html')
    Data = models.TimeTable.objects.all().values()
    if request.method == 'POST':
        Class = request.POST.get('Class')
        TimeTable = request.FILES.get('TimeTable')

        ClassExist = models.TimeTable.objects.filter(Class = Class)
        if not ClassExist:
            data = models.TimeTable.objects.create(Class = Class, Image = TimeTable)
            TimeTable = models.TimeTable.objects.all()
            data.save()
            context = {
                'success' : 'Successfully Uploaded Timetables',
                'TimeTable' : TimeTable,
            }
            return HttpResponse(AdminPage.render(context, request))
        else:
            data = models.TimeTable.objects.filter(Class = Class).first()
            data.Image = TimeTable
            data.save()
            context = {
                'success' : 'Successfully Uploaded Timetables'
            }
            return HttpResponse(AdminPage.render(context, request))
    context = {
        'error':'Error'
    }
    return HttpResponse(AdminPage.render(context, request))"""

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

"""def update_timetable(request):
    AdminPage = loader.get_template('AdminPage.html')
    if request.method == 'POST':
        Class = request.POST.get('Class')
        TimeTable = request.FILES.get('TimeTable')

        data, created = models.TimeTable.objects.update_or_create(Class=Class, defaults={'Image': TimeTable})

        context = {
            'success': 'Successfully Updated Timetables',
            'TimeTable': models.TimeTable.objects.all()
        }
        return HttpResponse(AdminPage.render(context, request))

    context = {
        'TimeTable': models.TimeTable.objects.all().values()
    }
    return HttpResponse(AdminPage.render(context, request))"""


