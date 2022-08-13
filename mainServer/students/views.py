from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse , HttpResponse
from . import models
import json
import datetime

# Create your views here.
def index(request):
    return render(request, "students/index.html")

def addStudent(request):
    context={}
    context['processed']=False
    if request.method == "POST":
        firstName=request.POST.get("firstName",None)
        lastName=request.POST.get("lastName",None)
        std=request.POST.get("std",None)
        sec=request.POST.get("sec",None)
        dob=request.POST.get("dob",None)
        address=request.POST.get("address",None)
        try:
            std=int(std)
            sec=sec[0].upper()

            if firstName!=None and lastName!=None and std!=None and sec!=None and dob!=None and address!=None:
                stdModel=models.student(firstName=firstName,lastName=lastName,std=std,sec=sec,dob=dob,address=address)
                stdModel.save()
                context["adminNo"]=f"Previous Student adminNo:{stdModel.adminNo}"
                context['processed']=True
        except Exception as e:
            context={}
            context["err"]=e
            return render(request, "students/err.html",context)
    return render(request, "students/addStudent.html",context)

def updateStudentFirst(request):
    return render(request, "students/updateStudentFirst.html")

def updateStudent(request,adminNo):
    processed=False
    err=""
    msg=""
    model=models.student.objects.get(adminNo=adminNo)
    if request.method == "POST":
        firstName=request.POST.get("firstName",None)
        lastName=request.POST.get("lastName",None)
        std=request.POST.get("std",None)
        sec=request.POST.get("sec",None)
        dob=request.POST.get("dob",None)
        address=request.POST.get("address",None)
        d=dob.split("-")
        dob=datetime.date(int(d[0]),int(d[1]),int(d[2]))
        try:
            std=int(std)
            sec=sec[0].upper()
            if firstName!=None and lastName!=None and std!=None and sec!=None and dob!=None and address!=None:
                model.firstName=firstName
                model.lastName=lastName
                model.address=address
                model.sec=sec
                model.dob=dob
                model.std=std
                model.save()
                processed=True
                msg="Success"
            else:
                err="Feilds are not properly sent"
        except Exception as e:
            err=str(e)
            print(e)
            processed=False
    context={
        "adminNo":model.adminNo,
        "firstName":model.firstName,
        "lastName":model.lastName,
        "std":model.std,
        "sec":model.sec,
        "dob":model.dob.strftime("%Y-%m-%d"),
        "addr":model.address,
    }
    context["isErr"]=not processed
    if not processed:
        context["err"]=err
    context["msg"]=msg
    return render(request, "students/updateStudent.html",context)

class faceCascade(View):
    def get(self, request):
        cascades={
            "cascade":[]
        }
        adminNo=request.GET.get("adminNo",None)
        if adminNo==None:
            for cascade in models.faceCascade.objects.all():
                cascades["cascade"].append({
                    "student":cascade.student.adminNo,
                    "studentCascade":json.loads(cascade.cascade)
                })
        else:
            stdModel=models.student.objects.get(adminNo=int(adminNo))
            model=models.faceCascade.objects.get(student=stdModel)
            cascades["cascade"].append({
                "student":model.student.adminNo,
                "studentCascade":json.loads(model.cascade)
            })
        return JsonResponse(cascades)

@method_decorator(csrf_exempt,name="dispatch")
class studentAttendance(View):
    def post(self, request):
        absentStudents=json.loads(request.body)["absentStudents"]
        for absentStudent in absentStudents:
            std=models.student.objects.get(adminNo=absentStudent)
            models.attendanceAbsentStudent.objects.get_or_create(student=std,date=datetime.date.today())
        return HttpResponse("Success")