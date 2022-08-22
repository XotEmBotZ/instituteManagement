from django.db import models
from students import models as stdModels

# Create your models here.
class teachersComplaint(models.Model):
    statusChoices=[
        ("opened","Opened"),
        ("investigating","Invistigating Complaint"),
        ("infromed","Informed the respective authorities"),
        ("punishment","Punishment Giving")
    ]
    complaintId=models.BigAutoField(primary_key=True)
    student=models.ForeignKey(stdModels.student,on_delete=models.CASCADE)
    complaint=models.TextField()
    status=models.TextField(choices=statusChoices,default=statusChoices[0][0])
    date=models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.student.firstName}-{self.student.adminNo}-{self.complaint[:5]}-{self.status}"