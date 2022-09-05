from multiprocessing import context
from operator import mod
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from . import models
import datetime
from students import models as stdModels
# Create your views here.


def index(request):
    return render(request, "authority/index.html")


def addStudent(request):
    context = {}
    context['processed'] = False
    if request.method == "POST":
        firstName = request.POST.get("firstName", None)
        lastName = request.POST.get("lastName", None)
        std = request.POST.get("std", None)
        sec = request.POST.get("sec", None)
        dob = request.POST.get("dob", None)
        address = request.POST.get("address", None)
        try:
            std = int(std)
            sec = sec[0].upper()

            if firstName != None and lastName != None and std != None and sec != None and dob != None and address != None:
                stdModel = stdModels.student(
                    firstName=firstName, lastName=lastName, std=std, sec=sec, dob=dob, address=address)
                stdModel.save()
                context["adminNo"] = f"Previous Student adminNo:{stdModel.adminNo}"
                context['processed'] = True
        except Exception as e:
            context = {}
            context["err"] = e
            return render(request, "authority/err.html", context)
    return render(request, "authority/addStudent.html", context)


def updateStudentFirst(request):
    return render(request, "authority/updateStudentFirst.html")


def updateStudent(request, adminNo):
    processed = False
    err = ""
    msg = ""
    model = stdModels.student.objects.get(adminNo=adminNo)
    if request.method == "POST":
        firstName = request.POST.get("firstName", None)
        lastName = request.POST.get("lastName", None)
        std = request.POST.get("std", None)
        sec = request.POST.get("sec", None)
        dob = request.POST.get("dob", None)
        address = request.POST.get("address", None)
        d = dob.split("-")
        dob = datetime.date(int(d[0]), int(d[1]), int(d[2]))
        try:
            std = int(std)
            sec = sec[0].upper()
            if firstName != None and lastName != None and std != None and sec != None and dob != None and address != None:
                model.firstName = firstName
                model.lastName = lastName
                model.address = address
                model.sec = sec
                model.dob = dob
                model.std = std
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
        "std": model.std,
        "sec": model.sec,
        "dob": model.dob.strftime("%Y-%m-%d"),
        "addr": model.address,
    }
    context["isErr"] = not processed
    if not processed:
        context["err"] = err
    context["msg"] = msg
    return render(request, "authority/updateStudent.html", context)


class addComplaint(View):
    def get(self, request):
        context = {
            "stdDetailsCheck": False
        }
        return render(request, "authority/addComplaint.html", context)

    def post(self, request):
        context = {}
        studentAdminNo = request.POST.get("adminNo", None)
        try:
            studentModel = stdModels.student.objects.get(
                adminNo=studentAdminNo)
            context["adminNo"] = studentAdminNo if studentAdminNo != None else ""
            context["stdName"] = studentModel.firstName + \
                studentModel.lastName if studentAdminNo != None else ""
            context["stdClass"] = studentModel.std if studentAdminNo != None else ""
            context["stdSec"] = studentModel.sec if studentAdminNo != None else ""
            context["stdDetailsCheck"] = True
            isVerifiedStudent = request.POST.get(
                "studentDetailsCheck", None) == "True"
            if isVerifiedStudent:
                studentAdminNo = request.POST.get("adminNo", None)
                studentModel = stdModels.student.objects.get(
                    adminNo=studentAdminNo)
                complaintModel = models.authorityComplaint()
                complaintModel.student = studentModel
                complaintModel.complaint = request.POST.get("complaint", None)
                complaintModel.level = request.POST.get("complaintLevel", 1)
                complaintModel.save()
                context["msgPresent"] = True
                context["msg"] = f"Complaint Created with ID- {complaintModel.complaintId}"
            else:
                context["msgPresent"] = True
                context["msg"] = "Please Verify the Student AdminNo First!"
        except stdModels.student.DoesNotExist:
            studentAdminNo = None
            context["msgPresent"] = True
            context["msg"] = "Student Details Not Found!"
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
                "studentName": f"{complaint.student.firstName} {complaint.student.lastName}",
                "studentStdSec": f"{complaint.student.std}-{complaint.student.sec}",
                "complaintLevel": complaint.level,
                "studentAdminNo": complaint.student.adminNo
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
                else:
                    context["msgPresent"] = True
                    context["msg"] = "Please provide complaint text and complaint status"
            complaint = models.authorityComplaint.objects.get(
                complaintId=complaintId)
            context["adminNo"] = complaint.student.adminNo
            context["stdName"] = complaint.student.firstName + \
                " " + complaint.student.lastName
            context["stdClass"] = complaint.student.std
            context["stdSec"] = complaint.student.sec
            context["complaint"] = complaint.complaint
            context["complaintLevel"] = complaint.level
            context["complaintStatus"] = complaint.status
        except models.authorityComplaint.DoesNotExist:
            context["msgPresent"] = True
            context["msg"] = "Invalid complaint Id"
        return render(request, "authority/editComplaint.html", context)
    else:
        return render(request, "authority/editComplaintBase.html")


def viewStudent(request):
    context = {}
    adminNo = request.GET.get("adminNo", None)
    if adminNo:
        try:
            stdModel = stdModels.student.objects.get(adminNo=adminNo)
            context["stdName"] = f"{stdModel.firstName} {stdModel.lastName}"
            context["stdStd"] = stdModel.std
            context["stdSec"] = stdModel.sec
            context["stdDob"] = stdModel.dob
            context["stdAddress"] = stdModel.address
            context["stdJoiningDate"] = stdModel.joiningDate
            context["stdBehaviorScore"] = stdModel.behaviorScore
            if stdModel.behaviorScore >= 0 and stdModel.behaviorScore < 33:
                context["behaviorClass"] = "cRed"
            elif stdModel.behaviorScore >= 33 and stdModel.behaviorScore < 66:
                context["behaviorClass"] = "cYellow"
            elif stdModel.behaviorScore >= 66:
                context["behaviorClass"] = "cGreen"
            context["stdFound"] = True
            behaviorNotices=models.authorityBehaviorNotice.objects.filter(student=stdModel)
            if len(behaviorNotices) > 0:
                context["behaviorNotices"]=behaviorNotices
                context["behaviorNoticePresent"]=True
            else:
                context["behaviorNoticePresent"]=False
        except stdModels.student.DoesNotExist:
            context["msgPresent"] = True
            context["msg"] = "Student not found. Please check the adminNo"
        return render(request, "authority/viewStudent.html", context)
    else:
        stdModels1 = stdModels.student.objects.all()
        if request.method == "POST":
            stdStd = request.POST.get("stdStd", None)
            stdSec = request.POST.get("stdSec", None)
            stdBehaviroScoreUpperLimit = request.POST.get(
                "stdBehaviroScoreUpperLimit", None)
            stdBehaviroScoreLowerLimit = request.POST.get(
                "stdBehaviroScoreLowerLimit", None)
            if stdStd:
                stdModels1 = stdModels1.filter(std=(stdStd))
            if stdSec:
                stdModels1 = stdModels1.filter(sec=stdSec)
            if stdBehaviroScoreUpperLimit:
                stdModels1 = stdModels1.filter(
                    behaviorScore__lte=stdBehaviroScoreUpperLimit)
            if stdBehaviroScoreLowerLimit:
                stdModels1 = stdModels1.filter(
                    behaviorScore__gte=stdBehaviroScoreLowerLimit)
        context["stdModels"] = stdModels1
        return render(request, "authority/viewAllStudents.html", context)

def viewAllBehaviorNotice(request):
    context={}
    adminNo=request.GET.get("adminNo", None)
    if not adminNo:
        allBNotice=models.authorityBehaviorNotice.objects.all()
        context["allBehaviorNotice"]=allBNotice
    else:
        student=stdModels.student.objects.get(adminNo=adminNo)
        allBNotice=models.authorityBehaviorNotice.objects.filter(student=student)
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