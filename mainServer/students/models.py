from ctypes import addressof
from django.db import models

# Create your models here.
class student(models.Model):
    adminNo=models.BigAutoField(primary_key=True)
    firstName = models.CharField(max_length=15)
    lastName = models.CharField(max_length=25)
    std=models.IntegerField()
    sec=models.CharField(max_length=1)
    dob=models.DateField()
    classRoll=models.IntegerField()
    address=models.TextField()
    joiningDate=models.DateField()

class parent(models.Model):
    student=models.ForeignKey(student, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=15)
    lastName = models.CharField(max_length=25)
    dob=models.DateField()
    phNo=models.IntegerField()
    occupation=models.TextField()
