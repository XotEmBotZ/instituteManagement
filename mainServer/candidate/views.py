from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from . import models
from authority import models as authorityModels

# Create your views here.
def index(request):
    return render(request, "candidate/index.html",)


class viewComplaint(View):
    def get(self, request):
        context = {"allComplaint": []}
        allComplaints = authorityModels.authorityComplaint.objects.all()
        for complaint in allComplaints:
            context["allComplaint"].append({
                "complaintId": complaint.complaintId,
                "complaint": complaint.complaint,
                "status": complaint.status,
                "candidateName": f"{complaint.candidate.firstName} {complaint.candidate.lastName}",
                "candidatecandSec": f"{complaint.candidate.cand}-{complaint.candidate.sec}",
                "complaintLevel": complaint.level,
                "candidateAdminNo":complaint.candidate.adminNo
            })
        return render(request, "candidate/viewComplaint.html", context)


def viewcandidate(request):
    context={}
    adminNo=request.GET.get("adminNo",None)
    if adminNo:
        try:
            candModel=models.candidate.objects.get(adminNo=adminNo)
            context["candName"]=f"{candModel.firstName} {candModel.lastName}"
            context["candcand"]=candModel.cand
            context["candSec"]=candModel.sec
            context["candDob"]=candModel.dob
            context["candAddress"]=candModel.address
            context["candJoiningDate"]=candModel.joiningDate
            context["candBehaviorScore"]=candModel.behaviorScore
            if candModel.behaviorScore>=0 and candModel.behaviorScore<33:
                context["behaviorClass"]="cRed"
            elif candModel.behaviorScore>=33 and candModel.behaviorScore<66:
                context["behaviorClass"]="cYellow"
            elif candModel.behaviorScore>=66:
                context["behaviorClass"]="cGreen"
            context["candFound"]=True
        except models.candidate.DoesNotExist:
            context["msgPresent"]=True
            context["msg"]="candidate not found. Please check the adminNo"
        return render(request, "candidate/viewCandidate.html",context)
    else:
        cand_models=models.candidate.objects.all()
        if request.method == "POST":
            candcand=request.POST.get("candcand",None)
            candSec=request.POST.get("candSec",None)
            candBehaviroScoreUpperLimit=request.POST.get("candBehaviroScoreUpperLimit",None)
            candBehaviroScoreLowerLimit=request.POST.get("candBehaviroScoreLowerLimit",None)
            if candcand:
                cand_models=cand_models.filter(cand=(candcand))
            if candSec:
                cand_models=cand_models.filter(sec=candSec)
            if candBehaviroScoreUpperLimit:
                cand_models=cand_models.filter(behaviorScore__lte=candBehaviroScoreUpperLimit)
            if candBehaviroScoreLowerLimit:
                cand_models=cand_models.filter(behaviorScore__gte=candBehaviroScoreLowerLimit)
        context["cand_models"]=cand_models
        return render(request, "candidate/viewAllCandidate.html",context)