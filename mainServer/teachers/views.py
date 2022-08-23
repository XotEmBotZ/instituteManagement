from django.shortcuts import render
from django.views import View
from . import models
import datetime
from students import models as stdModels
# Create your views here.


def index(request):
    return render(request, "teachers/index.html")

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
            return render(request, "teachers/err.html", context)
    return render(request, "teachers/addStudent.html", context)


def updateStudentFirst(request):
    return render(request, "teachers/updateStudentFirst.html")


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
    return render(request, "teachers/updateStudent.html", context)


class addComplaint(View):
    def get(self, request):
        context = {
            "stdDetailsCheck": False
        }
        return render(request, "teachers/addComplaint.html", context)

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
            context["stdDetailsCheck"]=True
            isVerifiedStudent=request.POST.get("studentDetailsCheck", None)=="True"
            if isVerifiedStudent:
                studentAdminNo = request.POST.get("adminNo", None)
                studentModel=stdModels.student.objects.get(adminNo=studentAdminNo)
                complaintModel=models.teachersComplaint()
                complaintModel.student=studentModel
                complaintModel.complaint=request.POST.get("complaint", None)
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
        return render(request, "teachers/addComplaint.html", context)

class viewComplaint(View):
    def get(self,request):
        context={"allComplaint":[]}
        allComplaints=models.teachersComplaint.objects.all()
        for complaint in allComplaints:
            context["allComplaint"].append({
                "complaintId":complaint.complaintId,
                "complaint":complaint.complaint,
                "status":complaint.status,
                "studentName":f"{complaint.student.firstName} {complaint.student.lastName}",
                "studentStdSec":f"{complaint.student.std}-{complaint.student.sec}"
            })
        return render(request,"teachers/viewComplaint.html",context)