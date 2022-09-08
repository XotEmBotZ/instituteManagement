from django.views.decorators.csrf import csrf_exempt
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
    adminNo=request.GET.get("adminNo",None)
    std=request.GET.get("std",None)
    sec=request.GET.get("sec",None)
    mdls=cand_models.candidate.objects.all()
    if adminNo:
        mdls=mdls.filter(adminNo=adminNo)
    if std:
        mdls=mdls.filter(std=std)
    if sec:
        mdls=mdls.filter(sec=sec)
    cascadeMdls=[]
    for cand in mdls:
        try:
            cascadeMdls.append(cand_models.candidateFaceCascade.objects.get(candidate=cand))
        except:
            pass
    for cascade in cascadeMdls:
        cascades["cascade"].append({
            "candidate": cascade.candidate.adminNo,
            "candidateCascade": json.loads(cascade.cascade)
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

def breakTime(request):
    try:
        adminNo=json.loads(request.body)["adminNo"]
        candModel=cand_models.candidate.objects.get(adminNo=adminNo)
        model,isCreated=cand_models.candidateBreakTime.objects.get_or_create(candidate=candModel,isEnded=False)
        if not isCreated:
            model.isEnded=True
            model.save()
        candModel.breakTime=datetime.timedelta()
        for bt in cand_models.candidateBreakTime.objects.filter(candidate=candModel,isEnded=True):
            candModel.breakTime+=bt.entryTime-bt.exitTime
        candModel.save()
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error","err":str(e)})

def testBgJob(request):
    bgJobs.sendBehaviorNotice()
    return JsonResponse({"status": "success"})

