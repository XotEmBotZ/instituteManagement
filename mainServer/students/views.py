from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from . import models
from teachers import models as teachersModels
import json
import datetime

# Create your views here.
def index(request):
    return render(request, "students/index.html",)


class viewComplaint(View):
    def get(self, request):
        context = {"allComplaint": []}
        allComplaints = teachersModels.teachersComplaint.objects.all()
        for complaint in allComplaints:
            context["allComplaint"].append({
                "complaintId": complaint.complaintId,
                "complaint": complaint.complaint,
                "status": complaint.status,
                "studentName": f"{complaint.student.firstName} {complaint.student.lastName}",
                "studentStdSec": f"{complaint.student.std}-{complaint.student.sec}",
                "complaintLevel": complaint.level,
                "studentAdminNo":complaint.student.adminNo
            })
        return render(request, "students/viewComplaint.html", context)


def viewStudent(request):
    context={}
    adminNo=request.GET.get("adminNo",None)
    if adminNo:
        try:
            stdModel=models.student.objects.get(adminNo=adminNo)
            context["stdName"]=f"{stdModel.firstName} {stdModel.lastName}"
            context["stdStd"]=stdModel.std
            context["stdSec"]=stdModel.sec
            context["stdDob"]=stdModel.dob
            context["stdAddress"]=stdModel.address
            context["stdJoiningDate"]=stdModel.joiningDate
            context["stdBehaviorScore"]=stdModel.behaviorScore
            if stdModel.behaviorScore>=0 and stdModel.behaviorScore<33:
                context["behaviorClass"]="cRed"
            elif stdModel.behaviorScore>=33 and stdModel.behaviorScore<66:
                context["behaviorClass"]="cYellow"
            elif stdModel.behaviorScore>=66:
                context["behaviorClass"]="cGreen"
        except models.student.DoesNotExist:
            context["msgPresent"]=True
            context["msg"]="Student not found. Please check the adminNo"
        return render(request, "students/viewStudent.html",context)
    # else:
    #     return render(request, "students/viewStudent.html",)
    return JsonResponse({"Status":"success"})