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
    Class = models.CharField(max_length=5)
    
    def __str__(self):
        return self.FullName
    


class Teacher(models.Model):
    FullName = models.CharField(max_length=100)
    MobileNo = models.CharField(max_length=10)
    Password = models.CharField(max_length=20)

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
    