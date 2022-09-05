from email.policy import default
from django.core.validators import MaxValueValidator, MinValueValidator
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
    behaviorScore=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],default=100)
    gainBehaviorScore=models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f"{self.adminNo}-{self.firstName} {self.lastName} - {self.std}{self.sec}"

class studentFaceCascade(models.Model):
    student=models.ForeignKey(student,on_delete=models.CASCADE)
    cascade=models.TextField()

    def __str__(self):
        return f"{self.student.firstName} {self.student.lastName}-{self.student.std}{self.student.sec}"

class studentAttendanceAbsentStudent(models.Model):
    student=models.ForeignKey(student,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.firstName} {self.student.lastName}-{self.student.std}{self.student.sec} {self.date}"