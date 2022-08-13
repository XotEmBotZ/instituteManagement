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
    address=models.TextField()
    joiningDate=models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.adminNo}-{self.firstName} {self.lastName} - {self.std}{self.sec}"

class parent(models.Model):
    student=models.ForeignKey(student, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=15)
    lastName = models.CharField(max_length=25)
    dob=models.DateField()
    phNo=models.IntegerField()
    occupation=models.TextField()

class faceCascade(models.Model):
    student=models.ForeignKey(student,on_delete=models.CASCADE)
    cascade=models.TextField()

    def __str__(self):
        return f"{self.student.firstName} {self.student.lastName}-{self.student.std}{self.student.sec}"

class attendanceAbsentStudent(models.Model):
    student=models.ForeignKey(student,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.firstName} {self.student.lastName}-{self.student.std}{self.student.sec} {self.date}"