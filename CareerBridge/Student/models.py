from django.db import models
from Admin import models as Amodels



class FeeDetails(models.Model):
    StudentRollNo = models.CharField(max_length=10)
    StudentName = models.CharField(max_length=30)
    Class = models.CharField(max_length=10)
    TotalFee = models.DecimalField(max_digits=10, decimal_places=2)
    Discount1 = models.DecimalField(max_digits=10, decimal_places=2)
    TotalPaidFee = models.DecimalField(max_digits=10, decimal_places=2)
    Due = models.DecimalField(max_digits=10, decimal_places=2)
    LatestPaidFee = models.DecimalField(max_digits=10, decimal_places=2)
    TransactionNo = models.CharField(max_length=30)

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

    def __str__(self):
        return self.StudentRollNo

