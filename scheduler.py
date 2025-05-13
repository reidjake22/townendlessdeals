# site_monitor/scheduler.py
import schedule
import time
from modules.checking.checker import checker
def start_scheduler():
    schedule.every(5).seconds.do(checker)
    print("Scheduler started.")
    while True:
        schedule.run_pending()
        time.sleep(1)
