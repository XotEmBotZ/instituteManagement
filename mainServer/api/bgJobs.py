from . import models
from students import models as std_models
from teachers import models as teachers_models
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
    allComplaint=teachers_models.teachersComplaint.objects.filter(isChecked=False,status="punishment")
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
    allStudents=std_models.student.objects.filter(behaviorScore__lt=100)
    for student in allStudents:
        student.behaviorScore+=1
        student.save()
schedule.every().day.at("12:00").do(run_threaded,gainBehaviorScore)

def deleteOldComplaint():
    teachers_models.teachersComplaint.objects.filter(date_lte=datetime.date()-datetime.timedelta(days=360),status="punishment").delete()
schedule.every().day.at("12:00").do(run_threaded,deleteOldComplaint)