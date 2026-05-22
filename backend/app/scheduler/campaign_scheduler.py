from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def reminder_job():
    print("Sending reminder calls...")

scheduler.add_job(
    reminder_job,
    "interval",
    minutes=1
)

scheduler.start()