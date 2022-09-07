from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from candidate import models as cand_models
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
        for cascade in cand_models.candidateFaceCascade.objects.all():
            cascades["cascade"].append({
                "candidate": cascade.candidate.adminNo,
                "candidateCascade": json.loads(cascade.cascade)
            })
    else:
        candModel = cand_models.candidate.objects.get(adminNo=int(adminNo))
        model = cand_models.candidateFaceCascade.objects.get(candidate=candModel)
        cascades["cascade"].append({
            "candidate": model.candidate.adminNo,
            "candidateCascade": json.loads(model.cascade)
        })
    return JsonResponse(cascades)


@csrf_exempt
def setAttendance(request):
    if request.method == "POST":
        absentcandidates = json.loads(request.body)["absentcandidates"]
        for absentcandidate in absentcandidates:
            cand = cand_models.candidate.objects.get(adminNo=absentcandidate)
            cand_models.candidateAttendanceAbsentcandidate.objects.get_or_create(
                candidate=cand, date=datetime.date.today())
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "HttpError"})

@csrf_exempt
def setFaceCascade(request):
    if request.method == "POST":
        try:
            jsonData = json.loads(request.body)
            candidateAdminNo = jsonData["adminNo"]
            candidateFaceCascade = jsonData["faceCascade"]
            candidateModel=cand_models.candidate.objects.get(adminNo=candidateAdminNo)
            model,created=cand_models.candidateFaceCascade.objects.get_or_create(candidate=candidateModel)
            model.cascade=json.dumps(candidateFaceCascade)
            model.save()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "err","err":str(e)})
    else:
        return JsonResponse({"status": "HttpErr"})

@csrf_exempt
def recordAttendance(request):
    try:
        candAdminNo=json.loads(request.body)["adminNo"]
        candModel=cand_models.candidate.objects.get(adminNo=candAdminNo)
        models.temporaryAttendance.objects.get_or_create(candidate=candModel)
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "failed","err":str(e)},status=406)

def testBgJob(request):
    bgJobs.sendBehaviorNotice()
    return JsonResponse({"status": "success"})

