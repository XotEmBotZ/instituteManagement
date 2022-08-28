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


class faceCascade(View):
    def get(self, request):
        cascades = {
            "cascade": []
        }
        adminNo = request.GET.get("adminNo", None)
        if adminNo == None:
            for cascade in models.studentFaceCascade.objects.all():
                cascades["cascade"].append({
                    "student": cascade.student.adminNo,
                    "studentCascade": json.loads(cascade.cascade)
                })
        else:
            stdModel = models.student.objects.get(adminNo=int(adminNo))
            model = models.studentFaceCascade.objects.get(student=stdModel)
            cascades["cascade"].append({
                "student": model.student.adminNo,
                "studentCascade": json.loads(model.cascade)
            })
        return JsonResponse(cascades)


@method_decorator(csrf_exempt, name="dispatch")
class studentAttendance(View):
    def post(self, request):
        absentStudents = json.loads(request.body)["absentStudents"]
        for absentStudent in absentStudents:
            std = models.student.objects.get(adminNo=absentStudent)
            models.studentAttendanceAbsentStudent.objects.get_or_create(
                student=std, date=datetime.date.today())
        return HttpResponse("Success")


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
