from multiprocessing import context
from operator import mod
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from . import models
import datetime
from candidate import models as cand_models
# Create your views here.


def index(request):
    return render(request, "authority/index.html")


def addcandidate(request):
    context = {}
    context['processed'] = False
    if request.method == "POST":
        firstName = request.POST.get("firstName", None)
        lastName = request.POST.get("lastName", None)
        cand = request.POST.get("cand", None)
        sec = request.POST.get("sec", None)
        dob = request.POST.get("dob", None)
        address = request.POST.get("address", None)
        try:
            cand = int(cand)
            sec = sec[0].upper()

            if firstName != None and lastName != None and cand != None and sec != None and dob != None and address != None:
                candModel = cand_models.candidate(
                    firstName=firstName, lastName=lastName, cand=cand, sec=sec, dob=dob, address=address)
                candModel.save()
                context["adminNo"] = f"Previous candidate adminNo:{candModel.adminNo}"
                context['processed'] = True
        except Exception as e:
            context = {}
            context["err"] = e
            return render(request, "authority/err.html", context)
    return render(request, "authority/addCandidate.html", context)


def updatecandidateFirst(request):
    return render(request, "authority/updateCandidateFirst.html")


def updatecandidate(request, adminNo):
    processed = False
    err = ""
    msg = ""
    model = cand_models.candidate.objects.get(adminNo=adminNo)
    if request.method == "POST":
        firstName = request.POST.get("firstName", None)
        lastName = request.POST.get("lastName", None)
        cand = request.POST.get("cand", None)
        sec = request.POST.get("sec", None)
        dob = request.POST.get("dob", None)
        address = request.POST.get("address", None)
        d = dob.split("-")
        dob = datetime.date(int(d[0]), int(d[1]), int(d[2]))
        try:
            cand = int(cand)
            sec = sec[0].upper()
            if firstName != None and lastName != None and cand != None and sec != None and dob != None and address != None:
                model.firstName = firstName
                model.lastName = lastName
                model.address = address
                model.sec = sec
                model.dob = dob
                model.cand = cand
                model.save()
                processed = True
                msg = "Success"
            else:
                err = "Feilds are not properly sent"
        except Exception as e:
            err = str(e)
            print(e)
            processed = False
    context = {
        "adminNo": model.adminNo,
        "firstName": model.firstName,
        "lastName": model.lastName,
        "cand": model.cand,
        "sec": model.sec,
        "dob": model.dob.strftime("%Y-%m-%d"),
        "addr": model.address,
    }
    context["isErr"] = not processed
    if not processed:
        context["err"] = err
    context["msg"] = msg
    return render(request, "authority/updateCandidate.html", context)


class addComplaint(View):
    def get(self, request):
        context = {
            "candDetailsCheck": False
        }
        return render(request, "authority/addComplaint.html", context)

    def post(self, request):
        context = {}
        candidateAdminNo = request.POST.get("adminNo", None)
        try:
            candidateModel = cand_models.candidate.objects.get(
                adminNo=candidateAdminNo)
            context["adminNo"] = candidateAdminNo if candidateAdminNo != None else ""
            context["candName"] = candidateModel.firstName + \
                candidateModel.lastName if candidateAdminNo != None else ""
            context["candClass"] = candidateModel.cand if candidateAdminNo != None else ""
            context["candSec"] = candidateModel.sec if candidateAdminNo != None else ""
            context["candDetailsCheck"] = True
            isVerifiedcandidate = request.POST.get(
                "candidateDetailsCheck", None) == "True"
            if isVerifiedcandidate:
                candidateAdminNo = request.POST.get("adminNo", None)
                candidateModel = cand_models.candidate.objects.get(
                    adminNo=candidateAdminNo)
                complaintModel = models.authorityComplaint()
                complaintModel.candidate = candidateModel
                complaintModel.complaint = request.POST.get("complaint", None)
                complaintModel.level = request.POST.get("complaintLevel", 1)
                complaintModel.save()
                context["msgPresent"] = True
                context["msg"] = f"Complaint Created with ID- {complaintModel.complaintId}"
            else:
                context["msgPresent"] = True
                context["msg"] = "Please Verify the candidate AdminNo First!"
        except cand_models.candidate.DoesNotExist:
            candidateAdminNo = None
            context["msgPresent"] = True
            context["msg"] = "candidate Details Not Found!"
        return render(request, "authority/addComplaint.html", context)


class viewComplaint(View):
    def get(self, request):
        context = {"allComplaint": []}
        allComplaints = models.authorityComplaint.objects.all()
        for complaint in allComplaints:
            context["allComplaint"].append({
                "complaintId": complaint.complaintId,
                "complaint": complaint.complaint,
                "status": complaint.status,
                "candidateName": f"{complaint.candidate.firstName} {complaint.candidate.lastName}",
                "candidatecandSec": f"{complaint.candidate.cand}-{complaint.candidate.sec}",
                "complaintLevel": complaint.level,
                "candidateAdminNo": complaint.candidate.adminNo
            })
        return render(request, "authority/viewComplaint.html", context)


def editComplaint(request):
    complaintId = request.GET.get("complaintId", None)
    context = {}
    if complaintId != None:
        try:
            if request.method == "POST":
                complaint = models.authorityComplaint.objects.get(
                    complaintId=complaintId)
                complaintText = request.POST.get("complaint", None)
                complaintStatus = request.POST.get("complaintStatus", None)
                if complaintStatus != None and complaintText != None:
                    complaint.complaint = complaintText
                    complaint.status = complaintStatus
                    complaint.save()
                    print(complaint.status)
                else:
                    context["msgPresent"] = True
                    context["msg"] = "Please provide complaint text and complaint status"
            complaint = models.authorityComplaint.objects.get(
                complaintId=complaintId)
            context["adminNo"] = complaint.candidate.adminNo
            context["candName"] = complaint.candidate.firstName + \
                " " + complaint.candidate.lastName
            context["candClass"] = complaint.candidate.cand
            context["candSec"] = complaint.candidate.sec
            context["complaint"] = complaint.complaint
            context["complaintLevel"] = complaint.level
            context["complaintStatus"] = complaint.status
        except models.authorityComplaint.DoesNotExist:
            context["msgPresent"] = True
            context["msg"] = "Invalid complaint Id"
        return render(request, "authority/editComplaint.html", context)
    else:
        return render(request, "authority/editComplaintBase.html")


def viewcandidate(request):
    context = {}
    adminNo = request.GET.get("adminNo", None)
    if adminNo:
        try:
            candModel = cand_models.candidate.objects.get(adminNo=adminNo)
            context["candName"] = f"{candModel.firstName} {candModel.lastName}"
            context["candcand"] = candModel.cand
            context["candSec"] = candModel.sec
            context["candDob"] = candModel.dob
            context["candAddress"] = candModel.address
            context["candJoiningDate"] = candModel.joiningDate
            context["candBehaviorScore"] = candModel.behaviorScore
            if candModel.behaviorScore >= 0 and candModel.behaviorScore < 33:
                context["behaviorClass"] = "cRed"
            elif candModel.behaviorScore >= 33 and candModel.behaviorScore < 66:
                context["behaviorClass"] = "cYellow"
            elif candModel.behaviorScore >= 66:
                context["behaviorClass"] = "cGreen"
            context["candFound"] = True
            behaviorNotices=models.authorityBehaviorNotice.objects.filter(candidate=candModel)
            if len(behaviorNotices) > 0:
                context["behaviorNotices"]=behaviorNotices
                context["behaviorNoticePresent"]=True
            else:
                context["behaviorNoticePresent"]=False
        except cand_models.candidate.DoesNotExist:
            context["msgPresent"] = True
            context["msg"] = "candidate not found. Please check the adminNo"
        return render(request, "authority/viewCandidate.html", context)
    else:
        cand_models1 = cand_models.candidate.objects.all()
        if request.method == "POST":
            candcand = request.POST.get("candcand", None)
            candSec = request.POST.get("candSec", None)
            candBehaviroScoreUpperLimit = request.POST.get(
                "candBehaviroScoreUpperLimit", None)
            candBehaviroScoreLowerLimit = request.POST.get(
                "candBehaviroScoreLowerLimit", None)
            if candcand:
                cand_models1 = cand_models1.filter(cand=(candcand))
            if candSec:
                cand_models1 = cand_models1.filter(sec=candSec)
            if candBehaviroScoreUpperLimit:
                cand_models1 = cand_models1.filter(
                    behaviorScore__lte=candBehaviroScoreUpperLimit)
            if candBehaviroScoreLowerLimit:
                cand_models1 = cand_models1.filter(
                    behaviorScore__gte=candBehaviroScoreLowerLimit)
        context["cand_models"] = cand_models1
        return render(request, "authority/viewAllCandidate.html", context)

def viewAllBehaviorNotice(request):
    context={}
    adminNo=request.GET.get("adminNo", None)
    if not adminNo:
        allBNotice=models.authorityBehaviorNotice.objects.all()
        context["allBehaviorNotice"]=allBNotice
    else:
        candidate=cand_models.candidate.objects.get(adminNo=adminNo)
        allBNotice=models.authorityBehaviorNotice.objects.filter(candidate=candidate)
        context["allBehaviorNotice"]=allBNotice
    return render(request, "authority/viewAllBehaviorNotice.html", context)

def editBehaviorNotice(request):
    context = {}
    if request.method == "POST":
        furtherNotified=request.POST.get("furtherNotified", None)
        furtherNotified=bool(furtherNotified)
        id=request.POST.get("id",None)
        mdl=models.authorityBehaviorNotice.objects.get(id=id)
        mdl.furtherNotified=bool(furtherNotified)
        mdl.save()
        print(bool(furtherNotified))
    behaviorNoticeId=request.GET.get("behaviorNoticeId", None)
    if behaviorNoticeId:
        context["notice"]=True
        context["bNotice"]=models.authorityBehaviorNotice.objects.get(id=behaviorNoticeId)
    else:
        context["askId"]=True
    return render(request, "authority/editBehaviorNotice.html", context)