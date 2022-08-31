from django.db import models

# Create your models here.
class errs(models.Model):
    err=models.CharField(max_length=255)
    filename=models.CharField(max_length=255,default="")
    lineNo=models.IntegerField(default=0)