from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.hashers import check_password
from . import models
from django.contrib import messages
from Student import models as Smodels
from django.db import transaction

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
            UpdateFeeses = models.UpdateFee.objects.all()
            if user:
                context = {
                    'TimeTable' : TimeTable,
                    'Class' : Class,
                    'Subject' : Subject,
                    'FeeDetails': FeeDetails,
                    'Students' : Students,
                    'UpdateFeeses' : UpdateFeeses,
                    'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
                    'ExamType' : models.ExamType.objects.all(),
                    'teachers' : models.Teacher.objects.all(),
                    'TeacherTimetables' : models.TeacherTimetable.objects.all(),
                    'StudentsCount' : len(models.Student.objects.all()),
                    'EmployeesCount' : len(models.Teacher.objects.all())
                }
                AdminPage = loader.get_template("AdminPage1.html")
                return HttpResponse(AdminPage.render(context, request))
            else:
                context = {
                    'error' : "Username or Password is incorrect. Please enter correct valid details."
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
    AdminPage = loader.get_template("AdminPage1.html")
    TimeTable = models.TimeTable.objects.all()
    Subject = models.Subject.objects.all()
    Class = models.Class.objects.all()
    Students = models.Student.objects.all()
    FeeDetails = Smodels.FeeDetails.objects.all()
    UpdateFeeses = models.UpdateFee.objects.all()
    context = {
        'TimeTable' : TimeTable,
        'Class' : models.Class.objects.all(),
        'Subject' : Subject,
        'FeeDetails': FeeDetails,
        'Students' : Students,
        'UpdateFeeses' : UpdateFeeses,
        'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
        'ExamType' : models.ExamType.objects.all(),
        'teachers' : models.Teacher.objects.all(),
        'TeacherTimetables' : models.TeacherTimetable.objects.all(),
        'StudentsCount' : len(models.Student.objects.all()),
        'EmployeesCount' : len(models.Teacher.objects.all())
    }

    if request.method == 'POST':
        FullName = request.POST.get('SFullName')
        RollNo = request.POST.get('SRollNo')
        Class = request.POST.get('Class')

        if FullName == '' or RollNo == '' or Class == '':
            context = {
                'error' : "Enter Valid Details",
                'TimeTable' : TimeTable,
                'Class' : models.Class.objects.all(),
                'Subject' : Subject,
                'FeeDetails': FeeDetails,
                'Students' : Students,
                'UpdateFeeses' : UpdateFeeses,
                'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
                'ExamType' : models.ExamType.objects.all(),
                'teachers' : models.Teacher.objects.all(),
                'TeacherTimetables' : models.TeacherTimetable.objects.all(),
                'StudentsCount' : len(models.Student.objects.all()),
                'EmployeesCount' : len(models.Teacher.objects.all())
            }
            return HttpResponse(AdminPage.render(context,request))
        if models.Student.objects.filter(RollNo = RollNo.upper()):
            context = {
                'error' : "RollNo Already Exist",
                'TimeTable' : TimeTable,
                'Class' : models.Class.objects.all(),
                'Subject' : Subject,
                'FeeDetails': FeeDetails,
                'Students' : Students,
                'UpdateFeeses' : UpdateFeeses,
                'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
                'ExamType' : models.ExamType.objects.all(),
                'teachers' : models.Teacher.objects.all(),
                'TeacherTimetables' : models.TeacherTimetable.objects.all(),
                'StudentsCount' : len(models.Student.objects.all()),
                'EmployeesCount' : len(models.Teacher.objects.all())
            }
            return HttpResponse(AdminPage.render(context, request))
        Fee = models.UpdateFee.objects.filter(Class = Class).first()

        try:
            with transaction.atomic():
                data = models.Student(FullName = FullName.upper(), RollNo = RollNo.upper(), Password = RollNo.upper(), Class = Class)
                FeeDetails = Smodels.FeeDetails(StudentRollNo = RollNo.upper(), StudentName = FullName.upper(), Class = Class, TotalFee = Fee.Fee,Discount1 = 0, TotalPaidFee = 0, Due = 0, LatestPaidFee  = 0)
                data.save()
                FeeDetails.save()
                context['success'] = "Student Registered Successfully"
        except Exception as e:
            context['error'] = f"Error: {str(e)}"
            return HttpResponse(AdminPage.render(context, request))

    return HttpResponse(AdminPage.render(context, request))

def TeacherRegistration(request):
    AdminPage = loader.get_template("AdminPage1.html")
    TimeTable = models.TimeTable.objects.all()
    Subject = models.Subject.objects.all()
    Class = models.Class.objects.all().order_by('-Class')
    Students = models.Student.objects.all()
    FeeDetails = Smodels.FeeDetails.objects.all()
    UpdateFeeses = models.UpdateFee.objects.all()
    Subjects = models.Subject.objects.values().all()
    context = {
        'TimeTable' : TimeTable,
        'Class' : Class,
        'Subject' : Subject,
        'FeeDetails': FeeDetails,
        'Students' : Students,
        'UpdateFeeses' : UpdateFeeses,
        'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
        'Subjects' : Subjects,
        'ExamType' : models.ExamType.objects.all(),
        'teachers' : models.Teacher.objects.all(),
        'TeacherTimetables' : models.TeacherTimetable.objects.all(),
        'StudentsCount' : len(models.Student.objects.all()),
        'EmployeesCount' : len(models.Teacher.objects.all())
    }

    if request.method == 'POST':
        FullName = request.POST.get('TFullName')
        MobileNo = request.POST.get('TMobileNo')
        TeacherID = request.POST.get('TeacherID')
        ClassTeacher = request.POST.get('ClassTeacher')
        Subject = request.POST.get('Subject')

        if models.Teacher.objects.filter(TeacherID = TeacherID.upper()):
            context['error'] = "TeacherID already exists"
            return HttpResponse(AdminPage.render(context, request))
        if len(MobileNo) != 10:
            context['error'] = 'Enter valid mobile number '
            return HttpResponse(AdminPage.render(context, request)) 

        try:
            data = models.Teacher(FullName = FullName.upper(), MobileNo = MobileNo, Password = TeacherID.upper(), TeacherID = TeacherID.upper(), ClassTeacher = ClassTeacher, Subject = Subject)
            data.save()
            context['success'] = "Teacher Registered Successfully"
        except Exception as e:
            context['error'] = f"Error: {str(e)}"
            return HttpResponse(AdminPage.render(context, request))

    return HttpResponse(AdminPage.render(context, request))


        

        


def UploadImage(request):
    AdminPage = loader.get_template('AdminPage1.html')
    TimeTable = models.TimeTable.objects.all()
    Subject = models.Subject.objects.all()
    Class = models.Class.objects.all()
    Students = models.Student.objects.all()
    FeeDetails = Smodels.FeeDetails.objects.all()
    UpdateFeeses = models.UpdateFee.objects.all()
    if request.method == 'POST':
        Title = request.POST.get('Title')
        Description = request.POST.get('Description')
        Image = request.FILES.get('Image')
        data = models.Posters.objects.create(Title = Title, Description = Description, Image=Image)
        data.save()
        context = {
            'success':"Successfully Uploaded Updates",
            'TimeTable' : TimeTable,
            'Class' : Class,
            'Subject' : Subject,
            'FeeDetails': FeeDetails,
            'Students' : Students,
            'UpdateFeeses' : UpdateFeeses,
            'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
            'ExamType' : models.ExamType.objects.all(),
            'teachers' : models.Teacher.objects.all(),
            'TeacherTimetables' : models.TeacherTimetable.objects.all(),
            'StudentsCount' : len(models.Student.objects.all()),
            'EmployeesCount' : len(models.Teacher.objects.all())
        }
        return HttpResponse(AdminPage.render(context, request))
    return render(request, 'AdminPage.html')

def ImageList(request):
    image = models.Posters.objects.all()
    return render(request, 'StudentLogin.html', {'image': image})



def TimeTable(request):
    AdminPage = loader.get_template('AdminPage1.html')
    Data = models.TimeTable.objects.all().values()
    TimeTable = models.TimeTable.objects.all()
    Subject = models.Subject.objects.all()
    Class = models.Class.objects.all()
    Students = models.Student.objects.all()
    FeeDetails = Smodels.FeeDetails.objects.all()
    UpdateFeeses = models.UpdateFee.objects.all()
    
    if request.method == 'POST':
        Class1 = request.POST.get('Class')
        TimeTable1 = request.FILES.get('TimeTable')
        ClassExist = models.TimeTable.objects.filter(Class=Class1).first()
        if ClassExist:
            ClassExist.Class = Class1
            ClassExist.Image = TimeTable1
            ClassExist.save()
        else:
            Details = models.TimeTable(Class = Class1, Image = TimeTable1)
            Details.save()
            
        context = {
            'success': 'Successfully Uploaded Timetables',
            'TimeTable': models.TimeTable.objects.all(),
            'TimeTable' : TimeTable,
            'Class' : Class,
            'Subject' : Subject,
            'FeeDetails': FeeDetails,
            'Students' : Students,
            'UpdateFeeses' : UpdateFeeses,
            'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
            'ExamType' : models.ExamType.objects.all(),
            'teachers' : models.Teacher.objects.all(),
            'TeacherTimetables' : models.TeacherTimetable.objects.all(),
            'StudentsCount' : len(models.Student.objects.all()),
            'EmployeesCount' : len(models.Teacher.objects.all())
        }
        
        return HttpResponse(AdminPage.render(context, request))
    
    context = {
        'TimeTable': models.TimeTable.objects.all().values(),
        'TimeTable' : TimeTable,
        'Class' : Class,
        'Subject' : Subject,
        'FeeDetails': FeeDetails,
        'Students' : Students,
        'UpdateFeeses' : UpdateFeeses,
        'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
        'ExamType' : models.ExamType.objects.all(),
        'teachers' : models.Teacher.objects.all(),
        'TeacherTimetables' : models.TeacherTimetable.objects.all(),
        'StudentsCount' : len(models.Student.objects.all()),
        'EmployeesCount' : len(models.Teacher.objects.all())
    }
    
    return HttpResponse(AdminPage.render(context, request))

def DeleteTimetable(request):
    AdminPage = loader.get_template('AdminPage1.html')
    context = {
        'TimeTable' : models.TimeTable.objects.all(),
        'Class' : models.Class.objects.all(),
        'Subject' : models.Subject.objects.all(),
        'FeeDetails': Smodels.FeeDetails.objects.all(),
        'Students' : models.Student.objects.all(),
        'UpdateFeeses' : models.UpdateFee.objects.all(),
        'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
        'ExamType' : models.ExamType.objects.all(),
        'teachers' : models.Teacher.objects.all(),
        'TeacherTimetables' : models.TeacherTimetable.objects.all(),
        'StudentsCount' : len(models.Student.objects.all()),
        'EmployeesCount' : len(models.Teacher.objects.all())
    }
    if request.method == 'POST':
        Class = request.POST.get('Class')
        models.TimeTable.objects.filter(Class = Class).delete()
        context['success'] = 'Successfully Deleted'
        return HttpResponse(AdminPage.render(context, request))
    return HttpResponse(AdminPage.render(context, request))



def add_subject(request):
    AdminPage = loader.get_template('AdminPage1.html')
    TimeTable = models.TimeTable.objects.all()
    Subject = models.Subject.objects.all()
    Class = models.Class.objects.all()
    Students = models.Student.objects.all()
    FeeDetails = Smodels.FeeDetails.objects.all()
    UpdateFeeses = models.UpdateFee.objects.all()
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
                'Subject' : Subject,
                'FeeDetails': FeeDetails,
                'Students' : Students,
                'UpdateFeeses' : UpdateFeeses,
                'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
                'ExamType' : models.ExamType.objects.all(),
                'teachers' : models.Teacher.objects.all(),
                'TeacherTimetables' : models.TeacherTimetable.objects.all(),
                'StudentsCount' : len(models.Student.objects.all()),
                'EmployeesCount' : len(models.Teacher.objects.all())
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
            'Subject' : Subject,
            'FeeDetails': FeeDetails,
            'Students' : Students,
            'UpdateFeeses' : UpdateFeeses,
            'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
            'ExamType' : models.ExamType.objects.all(),
            'teachers' : models.Teacher.objects.all(),
            'TeacherTimetables' : models.TeacherTimetable.objects.all(),
            'StudentsCount' : len(models.Student.objects.all()),
            'EmployeesCount' : len(models.Teacher.objects.all())

        }
        return HttpResponse(AdminPage.render(context,request))

def delete_subject(request):
    AdminPage = loader.get_template('AdminPage1.html')
    if request.method == 'POST':
        subject_id = request.POST['subject_id']

        # Delete the subject
        models.Subject.objects.filter(id=subject_id).delete()
        TimeTable = models.TimeTable.objects.all()
        Subject = models.Subject.objects.all()
        Class = models.Class.objects.all()
        Students = models.Student.objects.all()
        FeeDetails = Smodels.FeeDetails.objects.all()
        UpdateFeeses = models.UpdateFee.objects.all()

        context = {
            'success' : "Subject deleted successfully",
            'error': "ADMIN",
            'TimeTable' : TimeTable,
            'Class' : Class,
            'Subject' : Subject,
            'FeeDetails': FeeDetails,
            'Students' : Students,
            'UpdateFeeses' : UpdateFeeses,
            'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
            'ExamType' : models.ExamType.objects.all(),
            'teachers' : models.Teacher.objects.all(),
            'TeacherTimetables' : models.TeacherTimetable.objects.all(),
            'StudentsCount' : len(models.Student.objects.all()),
            'EmployeesCount' : len(models.Teacher.objects.all())
        }
        return HttpResponse(AdminPage.render(context,request))
    
def UpdateFeeDetails(request):
    AdminPage = loader.get_template("AdminPage1.html")
    TimeTable = models.TimeTable.objects.all()
    Subject = models.Subject.objects.all()
    Class1 = models.Class.objects.all()
    Students = models.Student.objects.all()
    FeeDetails = Smodels.FeeDetails.objects.all()
    UpdateFeeses = models.UpdateFee.objects.all()
    context = {
        'TimeTable' : TimeTable,
        'Class' : Class1,
        'Subject' : Subject,
        'FeeDetails': FeeDetails,
        'Students' : Students,
        'UpdateFeeses' : UpdateFeeses,
        'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
        'ExamType' : models.ExamType.objects.all(),
        'teachers' : models.Teacher.objects.all(),
        'TeacherTimetables' : models.TeacherTimetable.objects.all(),
        'StudentsCount' : len(models.Student.objects.all()),
        'EmployeesCount' : len(models.Teacher.objects.all())
    }


    if request.method == 'POST':
        StudentRollNo = request.POST.get('StudentRollNo')
        StudentName = request.POST.get('StudentName')
        Class = request.POST.get('Class')
        TotalFee = request.POST.get('TotalFee')
        LatestPaidFee = request.POST.get('LatestPaidFee')
        TotalPaidFee = request.POST.get('TotalPaidFee111')
        Discount = request.POST.get('Discount')
        Due = request.POST.get('Due111')
        TransactionNo = request.POST.get('TransactionNo')
        Date = request.POST.get('date')

        StudentExist = Smodels.FeeDetails.objects.filter(StudentRollNo = StudentRollNo, StudentName = StudentName, Class = Class).first()
        TransactionHistoryExist = Smodels.TransactionHistory.objects.filter(TransactionNo=TransactionNo).first()
        TransactionHistory = Smodels.TransactionHistory(StudentRollNo = StudentRollNo, StudentName=StudentName,Class=Class,TotalFee=TotalFee,Discount1=Discount,TotalPaidFee=(float(TotalPaidFee)+float(LatestPaidFee)),Due=(float(Due)-float(LatestPaidFee)),LatestPaidFee=LatestPaidFee,TransactionNo=TransactionNo,Date = Date)
        
        if TransactionHistoryExist:
            context['error'] = 'Transaction No already entered' 
            return HttpResponse(AdminPage.render(context,request))

        try:
            with transaction.atomic():
                if StudentExist:
                    StudentExist.TotalFee = TotalFee
                    StudentExist.Discount1 = Discount
                    StudentExist.LatestPaidFee = LatestPaidFee
                    StudentExist.TotalPaidFee = float(StudentExist.TotalPaidFee) + float(LatestPaidFee)
                    StudentExist.Due = float(StudentExist.TotalFee) - float(StudentExist.TotalPaidFee) - float(StudentExist.Discount1)
                    
                    StudentExist.save()
                    TransactionHistory.save()
                    

                    context = {
                        'success' : "Fee updated successfully",
                        'TimeTable' : TimeTable,
                        'Class' : Class,
                        'Subject' : Subject,
                        'FeeDetails': FeeDetails,
                        'Students' : Students,
                        'UpdateFeeses' : UpdateFeeses,
                        'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
                        'ExamType' : models.ExamType.objects.all(),
                        'teachers' : models.Teacher.objects.all(),
                        'TeacherTimetables' : models.TeacherTimetable.objects.all(),
                        'StudentsCount' : len(models.Student.objects.all()),
                        'EmployeesCount' : len(models.Teacher.objects.all())

                    }
                    return HttpResponse(AdminPage.render(context, request))
                    return redirect('admin_login')
                else:
                    context = {
                        'error' : "Fee updation failed",
                        'TimeTable' : TimeTable,
                        'Class' : Class,
                        'Subject' : Subject,
                        'FeeDetails': FeeDetails,
                        'Students' : Students,
                        'UpdateFeeses' : UpdateFeeses,
                        'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
                        'ExamType' : models.ExamType.objects.all(),
                        'teachers' : models.Teacher.objects.all(),
                        'TeacherTimetables' : models.TeacherTimetable.objects.all(),
                        'StudentsCount' : len(models.Student.objects.all()),
                        'EmployeesCount' : len(models.Teacher.objects.all())
                    } 
                    return HttpResponse(AdminPage.render(context, request))
        except Exception as e:
            context['error'] = f"Error: {str(e)}"
            return HttpResponse(AdminPage.render(context, request))
    context = {
        'error' : "Error"
    }
    return HttpResponse(AdminPage.render(context,request))

def UpdateFees(request):
    AdminPage = loader.get_template('AdminPage1.html')
    TimeTable = models.TimeTable.objects.all()
    Subject = models.Subject.objects.all()
    Class = models.Class.objects.all()
    Students = models.Student.objects.all()
    FeeDetails = Smodels.FeeDetails.objects.all()
    UpdateFeeses = models.UpdateFee.objects.all()
    context = {
        'TimeTable' : TimeTable,
        'Class' : Class,
        'Subject' : Subject,
        'FeeDetails': FeeDetails,
        'Students' : Students,
        'UpdateFeeses' : UpdateFeeses,
        'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
        'ExamType' : models.ExamType.objects.all(),
        'teachers' : models.Teacher.objects.all(),
        'TeacherTimetables' : models.TeacherTimetable.objects.all(),
        'StudentsCount' : len(models.Student.objects.all()),
        'EmployeesCount' : len(models.Teacher.objects.all())
    }
    if request.method == 'POST':
        Class = request.POST.get('Class')
        Fee = request.POST.get('Fee')

        UpdateFee = models.UpdateFee.objects.filter(Class = Class).first()
        
        try:
            UpdateFee.Class = Class
            UpdateFee.Fee = Fee
            UpdateFee.save()
            context = {
                'success' : "Updated successfully",
                'TimeTable' : TimeTable,
                'Class' : Class,
                'Subject' : Subject,
                'FeeDetails': FeeDetails,
                'Students' : Students,
                'UpdateFeeses' : UpdateFeeses,
                'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
                'ExamType' : models.ExamType.objects.all(),
                'teachers' : models.Teacher.objects.all(),
                'TeacherTimetables' : models.TeacherTimetable.objects.all(),
                'StudentsCount' : len(models.Student.objects.all()),
                'EmployeesCount' : len(models.Teacher.objects.all())
            }
            return HttpResponse(AdminPage.render(context,request))
        except Exception as e:
            context['error'] = f"Error: {str(e)}"
            return HttpResponse(AdminPage.render(context, request))

def TransactionHistory(request):
    AdminPage = loader.get_template('AdminPage1.html')
    transactions = Smodels.TransactionHistory.objects.filter(StudentRollNo='101').first()
    context = {
        'transactions': transactions
    }
    return HttpResponse(AdminPage.render(context, request))

def ExamType(request):
    AdminPage = loader.get_template('AdminPage1.html')
    context = {
        'TimeTable' : models.TimeTable.objects.all(),
        'Class' : models.Class.objects.all(),
        'Subject' : models.Subject.objects.all(),
        'FeeDetails': Smodels.FeeDetails.objects.all(),
        'Students' : models.Student.objects.all(),
        'UpdateFeeses' : models.UpdateFee.objects.all(),
        'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
        'ExamType' : models.ExamType.objects.all(),
        'teachers' : models.Teacher.objects.all(),
        'TeacherTimetables' : models.TeacherTimetable.objects.all(),
        'StudentsCount' : len(models.Student.objects.all()),
        'EmployeesCount' : len(models.Teacher.objects.all())
    }
    Students = models.Student.objects.all()
    if request.method == 'POST':
        ExamType = request.POST.get('ExamType')

        if models.ExamType.objects.filter(ExamType = ExamType).exists():
            context['error'] = 'ExamType already exists'
            return HttpResponse(AdminPage.render(context, request))

        try:
            if Students:
                with transaction.atomic():
                    ExamTypeData = models.ExamType(ExamType = ExamType, StudentAccess = 'Declined', TeacherAccess = 'Declined') 
                    for student in Students:
                        Subjects = models.Subject.objects.filter(Class = student.Class).all()
                        for Subject in Subjects:
                            ExamMarksData = models.ExamMarks.objects.filter(StudentRollNo = student.RollNo, StudentName = student.FullName, Subject = Subject, ExamType = ExamType, Marks = '0')
                            if not ExamMarksData:
                                ExamMarksData = models.ExamMarks(StudentRollNo = student.RollNo, StudentName = student.FullName, Subject = Subject, Class = student.Class,ExamType = ExamType, Marks = '0')
                                ExamTypeData.save()
                                ExamMarksData.save()
                                
                                context['success'] = 'Successfully Created'
                            else:
                                continue
            else:
                context['error'] = "No Students Found"
        except Exception as e:
            context['error'] = f"Error: {str(e)}"
            return HttpResponse(AdminPage.render(context, request))
        return HttpResponse(AdminPage.render(context, request))
    
def ExamMarksAccess(request):
    AdminPage = loader.get_template('AdminPage1.html')
    context = {
        'TimeTable' : models.TimeTable.objects.all(),
        'Class' : models.Class.objects.all(),
        'Subject' : models.Subject.objects.all(),
        'FeeDetails': Smodels.FeeDetails.objects.all(),
        'Students' : models.Student.objects.all(),
        'UpdateFeeses' : models.UpdateFee.objects.all(),
        'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
        'ExamType' : models.ExamType.objects.all(),
        'teachers' : models.Teacher.objects.all(),
        'TeacherTimetables' : models.TeacherTimetable.objects.all(),
        'StudentsCount' : len(models.Student.objects.all()),
        'EmployeesCount' : len(models.Teacher.objects.all())
    }
    if 'Update' in request.POST:
        ExamType1 = request.POST.get('ExamType1')
        StudentAccess = request.POST.get('StudentAccess')
        TeacherAccess = request.POST.get('TeacherAccess')

        try:
            ExamTypeAccessExists = models.ExamType.objects.filter(ExamType = ExamType1).first()
            if ExamTypeAccessExists:
                ExamTypeAccessExists.StudentAccess = StudentAccess
                ExamTypeAccessExists.TeacherAccess = TeacherAccess
                ExamTypeAccessExists.save()
            else:
                print("asfasf")
        except Exception as e:
            context['error'] : f"Error: {str(e)}"
        
        return HttpResponse(AdminPage.render(context, request))
    if 'Delete' in request.POST:
        ExamType = request.POST.get('ExamType1')
        num = models.ExamMarks.objects.filter(ExamType = ExamType).first()
        try:
            with transaction.atomic():
                models.ExamType.objects.filter(ExamType=ExamType).delete()
                models.ExamMarks.objects.filter(ExamType = ExamType).delete()
        except Exception as e:
            context['error'] : f"Error: {str(e)}"

        return HttpResponse(AdminPage.render(context, request))
    return HttpResponse(AdminPage.render(context, request))
            

def TeacherTimetable(request):
    AdminPage = loader.get_template('AdminPage1.html')
    context = {
        'TimeTable' : models.TimeTable.objects.all(),
        'Class' : models.Class.objects.all(),
        'Subject' : models.Subject.objects.all(),
        'FeeDetails': Smodels.FeeDetails.objects.all(),
        'Students' : models.Student.objects.all(),
        'UpdateFeeses' : models.UpdateFee.objects.all(),
        'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
        'ExamType' : models.ExamType.objects.all(),
        'teachers' : models.Teacher.objects.all(),
        'TeacherTimetables' : models.TeacherTimetable.objects.all(),
        'StudentsCount' : len(models.Student.objects.all()),
        'EmployeesCount' : len(models.Teacher.objects.all())
    }
    if request.method == 'POST':
        TeacherID = request.POST.get('Teacher')
        TimeTable = request.FILES.get('TimeTable')

        TimetableExists = models.TeacherTimetable.objects.filter(TeacherID = TeacherID).first()
        try:
            if TimetableExists:
                TimetableExists.TeacherID = TeacherID
                TimetableExists.Timetable = TimeTable
                TimetableExists.save()
                context['success'] = 'Successfully Uploaded Timetable'
            else:
                details = models.TeacherTimetable(Timetable = TimeTable, TeacherID = TeacherID)
                details.save()
                context['sucess'] = 'Successfully Uploaded Timetable'
            
        except Exception as e:
            context['error'] : f"Error: {str(e)}"
        return HttpResponse(AdminPage.render(context, request))
    return HttpResponse(AdminPage.render(context, request)) 

def DeleteTeacherTimetable(request):
    AdminPage = loader.get_template('AdminPage1.html')
    context = {
        'TimeTable' : models.TimeTable.objects.all(),
        'Class' : models.Class.objects.all(),
        'Subject' : models.Subject.objects.all(),
        'FeeDetails': Smodels.FeeDetails.objects.all(),
        'Students' : models.Student.objects.all(),
        'UpdateFeeses' : models.UpdateFee.objects.all(),
        'TransactionHistory' : Smodels.TransactionHistory.objects.all(),
        'ExamType' : models.ExamType.objects.all(),
        'teachers' : models.Teacher.objects.all(),
        'TeacherTimetables' : models.TeacherTimetable.objects.all(),
        'StudentsCount' : len(models.Student.objects.all()),
        'EmployeesCount' : len(models.Teacher.objects.all())
    }
    if request.method == 'POST':
        TeacherID = request.POST.get('Teacher')
        TeacherExist = models.TeacherTimetable.objects.filter(TeacherID = TeacherID).first()

        if TeacherExist:
            TeacherExist.delete()
            context['success'] = 'Sucessfully Deleted Timetable'
        else:
            context['error'] = "Timetable Doesn't Exist"
        
        return HttpResponse(AdminPage.render(context, request))
    return HttpResponse(AdminPage.render(context, request)) 