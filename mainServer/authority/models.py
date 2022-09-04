from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from students import models as stdModels
# Create your models here.
class authorityComplaint(models.Model):
    statusChoices=[
        ("opened","Opened"),
        ("investigating","Invistigating Complaint"),
        ("punishment","Punishment Giving")
    ]
    complaintId=models.BigAutoField(primary_key=True)
    student=models.ForeignKey(stdModels.student,on_delete=models.CASCADE)
    complaint=models.TextField()
    status=models.TextField(choices=statusChoices,default=statusChoices[0][0])
    level=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],default=1)
    date=models.DateField(auto_now=True)
    isChecked=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.firstName}-{self.student.adminNo}-{self.complaint[:5]}-{self.status}"

class authorityBehaviorNotice(models.Model):
    student=models.ForeignKey(stdModels.student,on_delete=models.CASCADE)
    furtherNotified=models.BooleanField(default=False)
    isChecked=models.BooleanField(default=False)
    date=models.DateField(auto_now_add=True)