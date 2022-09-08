from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.candidate)
# admin.site.register(models.parent)
admin.site.register(models.candidateFaceCascade)
admin.site.register(models.candidateAttendanceAbsentcandidate)