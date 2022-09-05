from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from students import models as std_models
from . import models
import json
import datetime

from . import bgJobs
# Create your views here.


def getFaceCascade(request):
    cascades = {
        "cascade": []
    }
    adminNo = request.GET.get("adminNo", None)
    if adminNo == None:
        for cascade in std_models.studentFaceCascade.objects.all():
            cascades["cascade"].append({
                "student": cascade.student.adminNo,
                "studentCascade": json.loads(cascade.cascade)
            })
    else:
        stdModel = std_models.student.objects.get(adminNo=int(adminNo))
        model = std_models.studentFaceCascade.objects.get(student=stdModel)
        cascades["cascade"].append({
            "student": model.student.adminNo,
            "studentCascade": json.loads(model.cascade)
        })
    return JsonResponse(cascades)


@csrf_exempt
def setAttendance(request):
    if request.method == "POST":
        absentStudents = json.loads(request.body)["absentStudents"]
        for absentStudent in absentStudents:
            std = std_models.student.objects.get(adminNo=absentStudent)
            std_models.studentAttendanceAbsentStudent.objects.get_or_create(
                student=std, date=datetime.date.today())
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "HttpError"})

@csrf_exempt
def setFaceCascade(request):
    if request.method == "POST":
        try:
            jsonData = json.loads(request.body)
            studentAdminNo = jsonData["adminNo"]
            studentFaceCascade = jsonData["faceCascade"]
            studentModel=std_models.student.objects.get(adminNo=studentAdminNo)
            model,created=std_models.studentFaceCascade.objects.get_or_create(student=studentModel)
            model.cascade=json.dumps(studentFaceCascade)
            model.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "err","err":str(e)})
    else:
        return JsonResponse({"status": "HttpErr"})

@csrf_exempt
def recordAttendance(request):
    try:
        stdAdminNo=json.loads(request.body)["adminNo"]
        stdModel=std_models.student.objects.get(adminNo=stdAdminNo)
        models.temporaryAttendance.objects.get_or_create(student=stdModel)
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "failed","err":str(e)},status=406)

def testBgJob(request):
    bgJobs.clearBehaviorNotice()
    return JsonResponse({"status": "success"})

