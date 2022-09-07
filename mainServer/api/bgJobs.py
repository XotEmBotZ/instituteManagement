from . import models
from candidate import models as cand_models
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
        candModel=complaint.candidate
        candModel.behaviorScore-=complaint.level*10
        if candModel.behaviorScore<0:
            candModel.behaviorScore=0
        candModel.save()
        complaint.isChecked=True
        complaint.save()
schedule.every(30).minutes.do(run_threaded,calculateBehaviorScore)

def gainBehaviorScore():
    allcandidates=cand_models.candidate.objects.filter(behaviorScore__lt=100,gainBehaviorScore=True)
    for candidate in allcandidates:
        candidate.behaviorScore+=1
        candidate.save()
schedule.every().day.at("12:00").do(run_threaded,gainBehaviorScore)

def deleteOldComplaint():
    authorityModels.authorityComplaint.objects.filter(date_lte=datetime.date.today()-datetime.timedelta(days=360),status="punishment").delete()
schedule.every().day.at("12:00").do(run_threaded,deleteOldComplaint)

def calculateAttendance():
    allPresentcand=models.temporaryAttendance.objects.filter(date=datetime.date.today())
    allAbsentcand=cand_models.candidate.objects.all().exclude(candidate=allPresentcand)
    for cand in allAbsentcand:
        cand_models.candidateAttendanceAbsentcandidate(candidate=cand).save()
schedule.every().day.at("12:00").do(run_threaded,calculateAttendance)

def sendBehaviorNotice():
    cands_models=cand_models.candidate.objects.filter(behaviorScore__lte=5,gainBehaviorScore=True)
    for cands in cands_models:
        authorityModels.authorityBehaviorNotice(candidate=cands).save()
        cands.gainBehaviorScore=False
        cands.save()
schedule.every().day.at("12:00").do(run_threaded,sendBehaviorNotice)

def clearBehaviorNotice():
    behaviorNotice=authorityModels.authorityBehaviorNotice.objects.filter(isChecked=False,furtherNotified=True)
    for notice in behaviorNotice:
        notice.candidate.behaviorScore=100
        notice.candidate.gainBehaviorScore=True
        notice.candidate.save()
        notice.isChecked=True
        notice.save()
schedule.every().day.at("12:00").do(run_threaded,clearBehaviorNotice)

def deleteOldBehaviorNotice():
    authorityModels.authorityBehaviorNotice.objects.filter(date_lte=datetime.date.today()-datetime.timedelta(days=360),isChecked=True).delete()
schedule.every().day.at("12:00").do(run_threaded,deleteOldBehaviorNotice)