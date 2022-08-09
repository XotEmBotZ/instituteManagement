from django.shortcuts import render
from . import models


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

def updateStudent(request):
    pass