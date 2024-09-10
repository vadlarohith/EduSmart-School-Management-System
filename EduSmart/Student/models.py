from django.db import models
from Admin import models as Amodels
from datetime import date 



class FeeDetails(models.Model):
    StudentRollNo = models.CharField(max_length=10)
    StudentName = models.CharField(max_length=30)
    Class = models.CharField(max_length=10)
    TotalFee = models.DecimalField(max_digits=10, decimal_places=2)
    Discount1 = models.DecimalField(max_digits=10, decimal_places=2)
    TotalPaidFee = models.DecimalField(max_digits=10, decimal_places=2)
    Due = models.DecimalField(max_digits=10, decimal_places=2)
    LatestPaidFee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.StudentRollNo
    
class TransactionHistory(models.Model):
    StudentRollNo = models.CharField(max_length=10)
    StudentName = models.CharField(max_length=30)
    Class = models.CharField(max_length=10)
    TotalFee = models.DecimalField(max_digits=10, decimal_places=2)
    Discount1 = models.DecimalField(max_digits=10, decimal_places=2)
    TotalPaidFee = models.DecimalField(max_digits=10, decimal_places=2)
    Due = models.DecimalField(max_digits=10, decimal_places=2)
    LatestPaidFee = models.DecimalField(max_digits=10, decimal_places=2)
    TransactionNo = models.CharField(max_length=30)
    Date = models.DateField()

    def __str__(self):
        return self.StudentRollNo
    
class StudentDetails(models.Model):
    RollNo = models.CharField(max_length=10)
    FullName = models.CharField(max_length=20)
    Gender = models.CharField(max_length=10)
    MailId = models.EmailField(max_length=30)
    DOB = models.DateField()
    StudentMobileNo = models.CharField(max_length=12)
    Nationality = models.CharField(max_length=10)
    FatherName = models.CharField(max_length=30)
    FatherOccupation = models.CharField(max_length=50)
    FatherMobileNo = models.CharField(max_length=12)
    FatherMailId = models.EmailField()
    MotherName = models.CharField(max_length=30)
    MotherOccupation = models.CharField(max_length=50, null=True)
    MotherMobileNo = models.CharField(max_length=12, null=True)
    MotherMailId = models.EmailField(null=True)
    PermanentAddress = models.CharField(max_length=50)
    CurrentAddress = models.CharField(max_length=50)

    def __str__(self):
        return self.RollNo





