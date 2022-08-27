import sched
from students import models as std_models
from teachers import models as teachers_models
import schedule
import threading
import time

def run_threaded(job_func,*args,**kwargs):
    job_thread = threading.Thread(target=job_func,args=args,kwargs=kwargs)
    job_thread.start()

def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

def printTest(Text):
    time.sleep(10)

schedule.every(10).seconds.do(run_threaded,printTest,Text="Texts")
# #Start the background thread
# stop_run_continuously = run_continuously()
# # Stop the background thread
# stop_run_continuously.set()