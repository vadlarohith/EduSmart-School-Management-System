from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.hashers import check_password
from Admin import models
from . import models as Smodels
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from django.db import transaction

def StudentLogin(request):
    StudentPage = loader.get_template("StudentLogin.html")
    HomePage = loader.get_template("home.html")
    Data = models.Student.objects.all().values()
    if request.method == 'POST':
        FullName = request.POST.get('StudentUserName')
        Password = request.POST.get('StudentPassword')
        SRegNo = request.POST.get('StudentRollNo')
 
        try:
            user = models.Student.objects.filter(FullName = FullName.upper(), Password = Password).first()
            if user:
                image = models.Posters.objects.all().values() 
                data = models.Student.objects.all()
                Class = user.Class
                TimeTable1 = models.TimeTable.objects.filter(Class = Class).first()
                Details = Smodels.StudentDetails.objects.filter(RollNo = user.RollNo, FullName = user.FullName).first()
                if(TimeTable1):
                    TimeTable = TimeTable1
                else:
                    TimeTable = None
                
                Subjects = models.Subject.objects.filter(Class = user.Class)
                FeeDetails = Smodels.FeeDetails.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName).first()

                 # Aggregate attendance by month for the student
                attendance_data = models.AttendenceDetails.objects.filter(RegNo=user.RollNo)\
                    .annotate(month=TruncMonth('AttendenceDate'))\
                    .values('month')\
                    .annotate(present_count=Count('Attendence', filter=Q(Attendence='P')))\
                    .annotate(absent_count=Count('Attendence', filter=Q(Attendence='A')))\
                    .annotate(total_count=Count('Attendence', filter=Q(Attendence__in=['P', 'A'])))\
                    .order_by('month')

                months = [entry['month'].strftime('%B') for entry in attendance_data]
                present_counts = [entry['present_count'] for entry in attendance_data]
                absent_counts = [entry['absent_count'] for entry in attendance_data]
                total_counts = [entry['total_count'] for entry in attendance_data]

                

                context = {
                    'Student': FullName,
                    'image' : image[::-1],
                    'data' : {
                        'FullName': user.FullName,
                        'RollNo' : user.RollNo,
                        'MobileNo': user.MobileNo,
                        'Password': user.Password,
                        'Class': user.Class,
                        'Profile' : user.Profile
                    },
                    'TimeTable' : TimeTable,
                    
                    'Subjects' : Subjects,
                    'FeeDetails' : FeeDetails,
                    'TotalFee' : FeeDetails.TotalFee - FeeDetails.Discount1,
                    'TransactionHistory' : Smodels.TransactionHistory.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName)[::-1],
                    'attendance_months': months,
                    'present_counts': present_counts,
                    'absent_counts': absent_counts,
                    'total_counts' : total_counts,
                    'ExamMarks' : models.ExamMarks.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName).values(),
                    'ExamType' : models.ExamType.objects.filter(StudentAccess = 'Accept').all(),

                }
                if Details:
                    context['details'] = {'Gender' : Details.Gender,
                    'DOB' : Details.DOB,
                    'MailId' : Details.MailId,
                    'Nationality' : Details.Nationality,
                    'FatherName' : Details.FatherName,
                    'MotherName' : Details.MotherName,
                    'FatherMobileNo' : Details.FatherMobileNo,
                    'MotherMobileNo' : Details.MotherMobileNo,
                    'FatherOccupation' : Details.FatherOccupation,
                    'MotherOccupation' : Details.MotherOccupation,
                    'FatherMailId' : Details.FatherMailId,
                    'MotherMailId' : Details.MotherMailId,
                    'PermanentAddress' : Details.PermanentAddress,
                    'CurrentAddress' : Details.CurrentAddress}
                return HttpResponse(StudentPage.render(context, request))
            else:
                context = {
                    'error' : "Username or Password is incorrect. Please enter correct valid details."
                }
                return HttpResponse(HomePage.render(context, request))
            
        except Exception as e:
            context['error'] = f"Error11: {str(e)}"
            return HttpResponse(HomePage.render(context, request))
        
def UpdateDetails(request):
    StudentPage = loader.get_template('StudentLogin.html')
    FeeDetails = Smodels.FeeDetails.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName).first()
    if request.method == 'POST': 
        FullName = request.POST.get('StudentName')
        RollNo = request.POST.get('StudentRollNo')
        UpdateMobileNo = request.POST.get('UpdateMobileNo')
        UpdatePassword = request.POST.get('UpdatePassword')

        
        
        try:
            image = models.Posters.objects.all()
            user = models.Student.objects.filter(FullName = FullName, RollNo = RollNo).first()
            Class = user.Class
            TimeTable1 = models.TimeTable.objects.filter(Class = Class).first()
            Details = Smodels.StudentDetails.objects.filter(RollNo = RollNo, FullName = user.FullName).first()
            if(TimeTable1):
                TimeTable = TimeTable1
            else:
                TimeTable = None
            #Attendence = models.Attendence.objects.filter(RegNo = user.RollNo)
            user.MobileNo = UpdateMobileNo
            user.Password = UpdatePassword
            user.save()
            context = {
                'success' : 'Successfully Updated',
                'Student': FullName,
                    'image' : image[::-1],
                    'data' : {
                        'FullName': user.FullName,
                        'RollNo' : user.RollNo,
                        'MobileNo': user.MobileNo,
                        'Password': user.Password,
                        'Class': user.Class,
                        'Profile' : user.Profile
                    },
                    'TimeTable' : TimeTable,
                    'TotalFee' : FeeDetails.TotalFee - FeeDetails.Discount1,
                    'TransactionHistory' : Smodels.TransactionHistory.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName).first()[::-1],
                    'ExamType' : models.ExamType.objects.filter(StudentAccess = 'Accept').all(),
                    
                    #'Attendence' : Attendence
            }
            if Details:
                context['details'] = {'Gender' : Details.Gender,
                    'DOB' : Details.DOB,
                    'MailId' : Details.MailId,
                    'Nationality' : Details.Nationality,
                    'FatherName' : Details.FatherName,
                    'MotherName' : Details.MotherName,
                    'FatherMobileNo' : Details.FatherMobileNo,
                    'MotherMobileNo' : Details.MotherMobileNo,
                    'FatherOccupation' : Details.FatherOccupation,
                    'MotherOccupation' : Details.MotherOccupation,
                    'FatherMailId' : Details.FatherMailId,
                    'MotherMailId' : Details.MotherMailId,
                    'PermanentAddress' : Details.PermanentAddress,
                    'CurrentAddress' : Details.CurrentAddress}
            return HttpResponse(StudentPage.render(context, request))
        
        except Exception as e:
            context['Success'] = f"Error: {str(e)}"
            return HttpResponse(StudentPage.render(context,request))
        
def Attendence(request):
    StudentPage = loader.get_template('StudentLogin.html')
    image = models.Posters.objects.all().values()
    context = {}
    if request.method == 'POST':
        StudentRollNo = request.POST.get('StudentRollNo')
        StudentName = request.POST.get('StudentName')
        FromDate = request.POST.get('fromDate')
        ToDate = request.POST.get('toDate')
        FYear, FMonth, FDate = FromDate.split('-')
        TYear, TMonth, TDate = ToDate.split('-')
        user = models.Student.objects.filter(FullName = StudentName, RollNo = StudentRollNo).first()
        TimeTable1 = models.TimeTable.objects.filter(Class = user.Class).first()
        Details = Smodels.StudentDetails.objects.filter(RollNo = user.RollNo, FullName = user.FullName).first()
        if(TimeTable1):
            TimeTable = TimeTable1
        else:
            TimeTable = None
        Subjects = models.Subject.objects.filter(Class = user.Class)
        FeeDetails = Smodels.FeeDetails.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName).first()
        Data = models.AttendenceDetails.objects.filter(RegNo = StudentRollNo, AttendenceDate__gte= FromDate , AttendenceDate__lte= ToDate).values()
        PresentDays1 = models.AttendenceDetails.objects.filter(RegNo = StudentRollNo, AttendenceDate__gte= FromDate, AttendenceDate__lte= ToDate, Attendence = 'P').values()
        TotalWorkingDays = Data.count()
        PresentDays = PresentDays1.count()

        attendance_data = models.AttendenceDetails.objects.filter(RegNo=user.RollNo)\
            .annotate(month=TruncMonth('AttendenceDate'))\
            .values('month')\
            .annotate(present_count=Count('Attendence', filter=Q(Attendence='P')))\
            .annotate(absent_count=Count('Attendence', filter=Q(Attendence='A')))\
            .annotate(total_count=Count('Attendence', filter=Q(Attendence__in=['P', 'A'])))\
            .order_by('month')

        months = [entry['month'].strftime('%B') for entry in attendance_data]
        present_counts = [entry['present_count'] for entry in attendance_data]
        absent_counts = [entry['absent_count'] for entry in attendance_data]
        total_counts = [entry['total_count'] for entry in attendance_data]

       

        context = {
            #'Date' : month1,
            #'Month' : month,
            'fromDate' : FromDate,
            'toDate' : ToDate,
            'WorkingDays' : TotalWorkingDays,
            'Present' : PresentDays,
            'image' : image[::-1],
            'data' : {
                'FullName': user.FullName,
                'RollNo' : user.RollNo,
                'MobileNo': user.MobileNo,
                'Password': user.Password,
                'Class': user.Class,
                'Profile' : user.Profile
            },
            'TimeTable' : TimeTable,
            
            'Subjects' : Subjects,
            'FeeDetails' : FeeDetails,
            'Percentage' : f"{(PresentDays/TotalWorkingDays)*100:.2f}",
            'TotalFee' : FeeDetails.TotalFee - FeeDetails.Discount1,
            'TransactionHistory' : Smodels.TransactionHistory.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName).all()[::-1],
            'attendance_months': months,
            'present_counts': present_counts,
            'absent_counts': absent_counts,
            'total_counts' : total_counts,
            'ExamMarks' : models.ExamMarks.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName).all(),
            'ExamType' : models.ExamType.objects.filter(StudentAccess = 'Accept').all(),
            

        }
        if Details:
            context['details'] = {'Gender' : Details.Gender,
                'DOB' : Details.DOB,
                'MailId' : Details.MailId,
                'Nationality' : Details.Nationality,
                'FatherName' : Details.FatherName,
                'MotherName' : Details.MotherName,
                'FatherMobileNo' : Details.FatherMobileNo,
                'MotherMobileNo' : Details.MotherMobileNo,
                'FatherOccupation' : Details.FatherOccupation,
                'MotherOccupation' : Details.MotherOccupation,
                'FatherMailId' : Details.FatherMailId,
                'MotherMailId' : Details.MotherMailId,
                'PermanentAddress' : Details.PermanentAddress,
                'CurrentAddress' : Details.CurrentAddress}
        return HttpResponse(StudentPage.render(context, request))
    
def ProfileUpdate(request):
    StudentPage = loader.get_template('StudentLogin.html')
    if request.method == 'POST':
        FullName = request.POST.get('FullName')
        RollNo = request.POST.get('RollNo')
        Profile = request.FILES.get('profileImage')

        user = models.Student.objects.filter(FullName = FullName, RollNo = RollNo).first()
        image = models.Posters.objects.all().values()
        Details = Smodels.StudentDetails.objects.filter(RollNo = RollNo, FullName = user.FullName).first()
        TimeTable1 = models.TimeTable.objects.filter(Class = user.Class).first()
        if(TimeTable1):
            TimeTable = TimeTable1
        else:
            TimeTable = None
        Subjects = models.Subject.objects.filter(Class = user.Class)
        FeeDetails = Smodels.FeeDetails.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName).first()

        attendance_data = models.AttendenceDetails.objects.filter(RegNo=user.RollNo)\
            .annotate(month=TruncMonth('AttendenceDate'))\
            .values('month')\
            .annotate(present_count=Count('Attendence', filter=Q(Attendence='P')))\
            .annotate(absent_count=Count('Attendence', filter=Q(Attendence='A')))\
            .annotate(total_count=Count('Attendence', filter=Q(Attendence__in=['P', 'A'])))\
            .order_by('month')

        months = [entry['month'].strftime('%B') for entry in attendance_data]
        present_counts = [entry['present_count'] for entry in attendance_data]
        absent_counts = [entry['absent_count'] for entry in attendance_data]
        total_counts = [entry['total_count'] for entry in attendance_data]
        

        context = {
            'Student': FullName,
            'image' : image[::-1],
            'data' : {
                'FullName': user.FullName,
                'RollNo' : user.RollNo,
                'MobileNo': user.MobileNo,
                'Password': user.Password,
                'Class': user.Class,
                'Profile' : user.Profile
            },
            'TimeTable' : TimeTable,
            
            'Subjects' : Subjects,
            'FeeDetails' : FeeDetails,
            'TotalFee' : FeeDetails.TotalFee - FeeDetails.Discount1,
            'TransactionHistory' : Smodels.TransactionHistory.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName)[::-1],
            'attendance_months': months,
            'present_counts': present_counts,
            'absent_counts': absent_counts,
            'total_counts' : total_counts,
            'ExamMarks' : models.ExamMarks.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName).all(),
            'ExamType' : models.ExamType.objects.filter(StudentAccess = 'Accept').all(),
            
        }
        if Details:
            context['details'] = {'Gender' : Details.Gender,
                'DOB' : Details.DOB,
                'MailId' : Details.MailId,
                'Nationality' : Details.Nationality,
                'FatherName' : Details.FatherName,
                'MotherName' : Details.MotherName,
                'FatherMobileNo' : Details.FatherMobileNo,
                'MotherMobileNo' : Details.MotherMobileNo,
                'FatherOccupation' : Details.FatherOccupation,
                'MotherOccupation' : Details.MotherOccupation,
                'FatherMailId' : Details.FatherMailId,
                'MotherMailId' : Details.MotherMailId,
                'PermanentAddress' : Details.PermanentAddress,
                'CurrentAddress' : Details.CurrentAddress}

        try:
            user.Profile = Profile
            user.save()
        except Exception as e:
            context['Success'] = f"Error: {str(e)}"

            return HttpResponse(StudentPage.render(context,request))
        return HttpResponse(StudentPage.render(context,request))
    
def ExamType(request):
    StudentPage = loader.get_template('StudentLogin.html')
    if request.method == 'POST':
        FullName = request.POST.get('FullName')
        RollNo = request.POST.get('RollNo')
        ExamType = request.POST.get('ExamType')

        user = models.Student.objects.filter(FullName = FullName, RollNo = RollNo).first()
        image = models.Posters.objects.all().values()
        Details = Smodels.StudentDetails.objects.filter(RollNo = RollNo, FullName = user.FullName).first()
        TimeTable1 = models.TimeTable.objects.filter(Class = user.Class).first()
        if(TimeTable1):
            TimeTable = TimeTable1
        else:
            TimeTable = None
        Subjects = models.Subject.objects.filter(Class = user.Class)
        FeeDetails = Smodels.FeeDetails.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName).first()

        attendance_data = models.AttendenceDetails.objects.filter(RegNo=user.RollNo)\
            .annotate(month=TruncMonth('AttendenceDate'))\
            .values('month')\
            .annotate(present_count=Count('Attendence', filter=Q(Attendence='P')))\
            .annotate(absent_count=Count('Attendence', filter=Q(Attendence='A')))\
            .annotate(total_count=Count('Attendence', filter=Q(Attendence__in=['P', 'A'])))\
            .order_by('month')

        months = [entry['month'].strftime('%B') for entry in attendance_data]
        present_counts = [entry['present_count'] for entry in attendance_data]
        absent_counts = [entry['absent_count'] for entry in attendance_data]
        total_counts = [entry['total_count'] for entry in attendance_data]

        MinMarks = 0
        for i in models.ExamType.objects.all():
            MinMarks = i.MaxMarks * 30 / 100
            break

        StudentRanks = {}
        for i in models.Student.objects.filter(Class = user.Class).all():
            TotalMarks = 0
            Status = 'Pass'
            for j in models.ExamMarks.objects.filter(ExamType = ExamType, StudentRollNo = i.RollNo, StudentName = i.FullName).all():
                TotalMarks += j.Marks
                if j.Marks < MinMarks:
                    Status = 'Fail'
            if Status == 'Pass':
                StudentRanks[i.RollNo] = TotalMarks
        #StudentRanks = dict(sorted(StudentRanks.items(), key=lambda item: item[1], reverse=True))
        StudentRanks = sorted(StudentRanks.items(), key=lambda item: item[1], reverse=True)
        #rank = list(StudentRanks.keys()).index(user.RollNo) + 1  #getting different ranks if two student get the same total marks

        ranks = {}
        current_rank = 1
        previous_marks = None

        for index, (RollNo, TotalMarks) in enumerate(StudentRanks):
            if TotalMarks != previous_marks:
                current_rank = index + 1  # Assign rank based on index if marks are different
            ranks[RollNo] = current_rank  # Assign the same rank to students with the same marks
            previous_marks = TotalMarks

        # Step 4: Get the rank of the specific student
        if user.RollNo in ranks:
            rank = ranks[user.RollNo]
        else:
            rank = 'F'


        TotalMarks = 0
        Marks = 0
        for i in models.ExamMarks.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName, ExamType = ExamType).all():
            TotalMarks += models.ExamType.objects.filter(ExamType = ExamType).first().MaxMarks
            Marks += i.Marks
        SubjectsForResults = []
        for i in Subjects:
            SubjectsForResults.append(i.Subject)
        MarksForResults = []
        for i in models.ExamMarks.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName, ExamType = ExamType).all():
            MarksForResults.append(i.Marks)
        
        context = {
            'Student': FullName,
            'image' : image[::-1],
            'data' : {
                'FullName': user.FullName,
                'RollNo' : user.RollNo,
                'MobileNo': user.MobileNo,
                'Password': user.Password,
                'Class': user.Class,
                'Profile' : user.Profile
            },
            'TimeTable' : TimeTable,
            
            'Subjects' : Subjects,
            'FeeDetails' : FeeDetails,
            'TotalFee' : FeeDetails.TotalFee - FeeDetails.Discount1,
            'TransactionHistory' : Smodels.TransactionHistory.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName)[::-1],
            'attendance_months': months,
            'present_counts': present_counts,
            'absent_counts': absent_counts,
            'total_counts' : total_counts,
            'ExamMarks' : models.ExamMarks.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName, ExamType = ExamType).all(),
            'ExamType' : models.ExamType.objects.filter(StudentAccess = 'Accept').all(),
            'DefaultExamType' : ExamType,
            'Marks' : {
                'TotalMarks' : TotalMarks,
                'Marks' : Marks,
                'Percentage' :round((Marks/TotalMarks)*100,2),
                'Rank' : rank,
                'Subjects1' : SubjectsForResults,
                'Marks1' : MarksForResults
            }


        }
        if Details:
            context['details'] = {'Gender' : Details.Gender,
                'DOB' : Details.DOB,
                'MailId' : Details.MailId,
                'Nationality' : Details.Nationality,
                'FatherName' : Details.FatherName,
                'MotherName' : Details.MotherName,
                'FatherMobileNo' : Details.FatherMobileNo,
                'MotherMobileNo' : Details.MotherMobileNo,
                'FatherOccupation' : Details.FatherOccupation,
                'MotherOccupation' : Details.MotherOccupation,
                'FatherMailId' : Details.FatherMailId,
                'MotherMailId' : Details.MotherMailId,
                'PermanentAddress' : Details.PermanentAddress,
                'CurrentAddress' : Details.CurrentAddress}
        return HttpResponse(StudentPage.render(context,request))
    return HttpResponse(StudentPage.render(context,request))

def ProfileDetailsUpdate(request):
    StudentPage = loader.get_template('StudentLogin.html')
    if request.method == 'POST':
        RollNo = request.POST.get('RollNo')
        StudentMobileNo = request.POST.get('StudentMobileNo')
        Gender = request.POST.get('Gender')
        Date = request.POST.get('DOB')
        StudentMailId = request.POST.get('StudentMailId')
        Nationality1 = request.POST.get('Nationality')
        FatherName = request.POST.get('FatherName')
        MotherName = request.POST.get('MotherName')
        FatherMobileNo = request.POST.get('FatherMobileNo')
        MotherMobileNo = request.POST.get('MotherMobileNo')
        FatherOccupation = request.POST.get('FatherOccupation')
        MotherOccupation = request.POST.get('MotherOccupation')
        FatherMailId = request.POST.get('FatherMailId')
        MotherMailId = request.POST.get('MotherMailId')
        PermanentAddress = request.POST.get('PermanentAddress')
        CurrentAddress = request.POST.get('CurrentAddress')

        user = models.Student.objects.filter(RollNo = RollNo).first()
        image = models.Posters.objects.all().values()
        TimeTable1 = models.TimeTable.objects.filter(Class = user.Class).first()
        if(TimeTable1):
            TimeTable = TimeTable1
        else:
            TimeTable = None
        Subjects = models.Subject.objects.filter(Class = user.Class)
        FeeDetails = Smodels.FeeDetails.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName).first()
        Details = Smodels.StudentDetails.objects.filter(RollNo = RollNo, FullName = user.FullName).first()

        attendance_data = models.AttendenceDetails.objects.filter(RegNo=user.RollNo)\
            .annotate(month=TruncMonth('AttendenceDate'))\
            .values('month')\
            .annotate(present_count=Count('Attendence', filter=Q(Attendence='P')))\
            .annotate(absent_count=Count('Attendence', filter=Q(Attendence='A')))\
            .annotate(total_count=Count('Attendence', filter=Q(Attendence__in=['P', 'A'])))\
            .order_by('month')

        months = [entry['month'].strftime('%B') for entry in attendance_data]
        present_counts = [entry['present_count'] for entry in attendance_data]
        absent_counts = [entry['absent_count'] for entry in attendance_data]
        total_counts = [entry['total_count'] for entry in attendance_data]
        
        
        context = {
            'Student': user.FullName,
            'image' : image[::-1],
            'data' : {
                'FullName': user.FullName,
                'RollNo' : user.RollNo,
                'MobileNo': user.MobileNo,
                'Password': user.Password,
                'Class': user.Class,
                'Profile' : user.Profile
            },
            'TimeTable' : TimeTable,
            
            'Subjects' : Subjects,
            'FeeDetails' : FeeDetails,
            'TotalFee' : FeeDetails.TotalFee - FeeDetails.Discount1,
            'TransactionHistory' : Smodels.TransactionHistory.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName)[::-1],
            'attendance_months': months,
            'present_counts': present_counts,
            'absent_counts': absent_counts,
            'total_counts' : total_counts,
            'ExamMarks' : models.ExamMarks.objects.filter(StudentRollNo = user.RollNo, StudentName = user.FullName).all(),
            'ExamType' : models.ExamType.objects.filter(StudentAccess = 'Accept').all(),
            
            
        }
        if Details:
            context['details'] = {'Gender' : Details.Gender,
                'DOB' : Details.DOB,
                'MailId' : Details.MailId,
                'Nationality' : Details.Nationality,
                'FatherName' : Details.FatherName,
                'MotherName' : Details.MotherName,
                'FatherMobileNo' : Details.FatherMobileNo,
                'MotherMobileNo' : Details.MotherMobileNo,
                'FatherOccupation' : Details.FatherOccupation,
                'MotherOccupation' : Details.MotherOccupation,
                'FatherMailId' : Details.FatherMailId,
                'MotherMailId' : Details.MotherMailId,
                'PermanentAddress' : Details.PermanentAddress,
                'CurrentAddress' : Details.CurrentAddress}
        
        try:
            with transaction.atomic():
                StudentExists = Smodels.StudentDetails.objects.filter(RollNo = RollNo).first()
                
                if StudentExists:
                    StudentExists.RollNo = RollNo
                    StudentExists.FullName = user.FullName
                    StudentExists.Gender = Gender
                    StudentExists.MailId = StudentMailId
                    StudentExists.DOB = Date
                    StudentExists.Nationality = Nationality1
                    StudentExists.FatherName = FatherName
                    StudentExists.FatherOccupation = FatherOccupation
                    StudentExists.FatherMobileNo = FatherMobileNo
                    StudentExists.FatherMailId = FatherMailId
                    StudentExists.MotherName = MotherName
                    StudentExists.MotherOccupation = MotherOccupation
                    StudentExists.MotherMobileNo = MotherMobileNo
                    StudentExists.MotherMailId = MotherMailId
                    StudentExists.PermanentAddress = PermanentAddress
                    StudentExists.CurrentAddress = CurrentAddress
                    StudentExists.save()
                    context['success'] = "Successfully Updated"
                else:
                    print("ha")
                    StudentProfile = Smodels.StudentDetails(RollNo = RollNo, FullName = user.FullName, Gender = Gender, MailId = StudentMailId, DOB = Date, Nationality = Nationality1, FatherName = FatherName, FatherOccupation = FatherOccupation, FatherMobileNo = FatherMobileNo, FatherMailId = FatherMailId, MotherName = MotherName, MotherOccupation = MotherOccupation, MotherMobileNo = MotherMobileNo, MotherMailId = MotherMailId, PermanentAddress = PermanentAddress, CurrentAddress = CurrentAddress)
                    print("hai")
                    StudentProfile.save()
                    print('ass')
                    context['success'] = "Successfully Updated"
                return HttpResponse(StudentPage.render(context,request))
        except Exception as e:
            context['Success'] = f"Error: {str(e)}"
        return HttpResponse(StudentPage.render(context,request))
    else:
        context['error'] = "Error"
    return HttpResponse(StudentPage.render(context,request))