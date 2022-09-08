from email.policy import default
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
class candidate(models.Model):
    adminNo=models.BigAutoField(primary_key=True)
    firstName = models.CharField(max_length=15)
    lastName = models.CharField(max_length=25)
    cand=models.IntegerField()
    sec=models.CharField(max_length=1)
    dob=models.DateField()
    address=models.TextField()
    joiningDate=models.DateField(auto_now_add=True)
    behaviorScore=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],default=100)
    gainBehaviorScore=models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f"{self.adminNo}-{self.firstName} {self.lastName} - {self.cand}{self.sec}"

class candidateFaceCascade(models.Model):
    candidate=models.ForeignKey(candidate,on_delete=models.CASCADE)
    cascade=models.TextField()

    def __str__(self):
        return f"{self.candidate.firstName} {self.candidate.lastName}-{self.candidate.cand}{self.candidate.sec}"

class candidateAttendanceAbsentcandidate(models.Model):
    candidate=models.ForeignKey(candidate,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.firstName} {self.candidate.lastName}-{self.candidate.cand}{self.candidate.sec} {self.date}"

class candidateBreakTime(models.Model):
    candidate=models.ForeignKey(candidate,on_delete=models.CASCADE)
    isEnded=models.BooleanField(default=False)
    exitTime=models.DateTimeField(auto_now_add=True)
    entryTime=models.DateTimeField(auto_now=True)