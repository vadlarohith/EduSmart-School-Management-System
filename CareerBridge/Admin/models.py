"""from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)"""

from django.db import models
from django.contrib.auth.hashers import make_password
from datetime import date 

class Admin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Student(models.Model):
    FullName = models.CharField(max_length=150)
    RollNo = models.CharField(max_length=10)
    Password = models.CharField(max_length=15)
    MobileNo = models.CharField(max_length=10)
    Class = models.CharField(max_length=7)
    Profile = models.ImageField(null=True, upload_to='Profile/')
    
    def __str__(self):
        return self.FullName
    


class Teacher(models.Model):
    TeacherID = models.CharField(max_length=10)
    FullName = models.CharField(max_length=100)
    MobileNo = models.CharField(max_length=10)
    Password = models.CharField(max_length=20)
    ClassTeacher = models.CharField(max_length=10)
    Subject = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.FullName
    
class Posters(models.Model):
    Title = models.CharField(max_length=100)
    Description = models.CharField(max_length=200)
    Image = models.ImageField(upload_to='image/')

    def __str__(self):
        return self.Title
    
class TimeTable(models.Model):
    Class = models.CharField(max_length=10)
    Image = models.ImageField(upload_to='image/')

    def __str__(self):
        return self.Class

    
class Attendence(models.Model):
    RegNo = models.CharField(max_length=10)
    Month = models.CharField(max_length=10)
    Attendence = models.CharField(max_length=10)

    def __str__(self):
        return self.RegNo
    
class Class(models.Model):
    Class = models.CharField(max_length=10)

    def __str__(self):
        return self.Class
    
class Subject(models.Model):
    Class = models.CharField(max_length=10)
    Subject = models.CharField(max_length=30)
    SubCode = models.CharField(max_length=10)

    def __str__(self):
        return self.Subject
    
class UpdateFee(models.Model):
    Class = models.CharField(max_length=10)
    Fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.Class
    
class AttendenceDetails(models.Model):
    RegNo = models.CharField(max_length=10)
    Attendence = models.CharField(max_length=5)
    AttendenceDate = models.DateField(default=date.today)

    def __str__(self):
        return self.RegNo
