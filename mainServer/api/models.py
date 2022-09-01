from datetime import datetime
from django.db import models
from students.models import student
# Create your models here.
class errs(models.Model):
    err=models.CharField(max_length=255)
    filename=models.CharField(max_length=255,default="")
    lineNo=models.IntegerField(default=0)

class temporaryAttendance(models.Model):
    student=models.ForeignKey(student,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)