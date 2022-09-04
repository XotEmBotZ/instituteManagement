from . import models
from students import models as std_models
from authority import models as authorityModels
import datetime
import schedule
from multiprocessing import Process
import threading
import time

def run_threaded(job_func,*args,**kwargs):
    job_thread = threading.Thread(target=job_func,args=args,kwargs=kwargs)
    job_thread.start()

def runSchedule(interval=1):
    while True:
        schedule.run_pending()
        time.sleep(interval)

def run_continuously(interval=1):
    thread=threading.Thread(target=runSchedule,args=(interval,))
    thread.setDaemon(True)
    thread.start()

def calculateBehaviorScore():
    allComplaint=authorityModels.authorityComplaint.objects.filter(isChecked=False,status="punishment")
    print(allComplaint)
    for complaint in allComplaint:
        stdModel=complaint.student
        stdModel.behaviorScore-=complaint.level*10
        if stdModel.behaviorScore<0:
            stdModel.behaviorScore=0
        stdModel.save()
        complaint.isChecked=True
        complaint.save()
schedule.every(30).minutes.do(run_threaded,calculateBehaviorScore)

def gainBehaviorScore():
    allStudents=std_models.student.objects.filter(behaviorScore__lt=100,gainBehaviorScore=True)
    for student in allStudents:
        student.behaviorScore+=1
        student.save()
schedule.every().day.at("12:00").do(run_threaded,gainBehaviorScore)

def deleteOldComplaint():
    authorityModels.authorityComplaint.objects.filter(date_lte=datetime.date.today()-datetime.timedelta(days=360),status="punishment").delete()
schedule.every().day.at("12:00").do(run_threaded,deleteOldComplaint)

def calculateAttendance():
    allPresentStd=models.temporaryAttendance.objects.filter(date=datetime.date.today())
    allAbsentStd=std_models.student.objects.all().exclude(student=allPresentStd)
    for std in allAbsentStd:
        std_models.studentAttendanceAbsentStudent(student=std).save()
schedule.every().day.at("12:00").do(run_threaded,calculateAttendance)

def sendBehaviorNotice():
    stdModels=std_models.student.objects.filter(behaviorScore__lte=5,gainBehaviorScore=True)
    for std in stdModels:
        authorityModels.authorityBehaviorNotice(student=std).save()
        std.gainBehaviorScore=False
        std.save()
schedule.every().day.at("12:00").do(run_threaded,sendBehaviorNotice)

def clearBehaviorNotice():
    behaviorNotice=authorityModels.authorityBehaviorNotice.objects.filter(isChecked=False,furtherNotified=True)
    for notice in behaviorNotice:
        notice.student.behaviorScore=100
        notice.student.gainBehaviorScore=True
        notice.student.save()
        notice.isChecked=True
        notice.save()
schedule.every().day.at("12:00").do(run_threaded,clearBehaviorNotice)

def deleteOldBehaviorNotice():
    authorityModels.authorityBehaviorNotice.objects.filter(date_lte=datetime.date.today()-datetime.timedelta(days=360),isChecked=True).delete()
schedule.every().day.at("12:00").do(run_threaded,deleteOldBehaviorNotice)