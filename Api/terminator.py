import schedule
import datetime
from .models import Link
import time

print('terminator running ...')

def job():
    now = datetime.datetime.now()
    Link.objects.filter(expiration_date__date=now.date()).update(expired=True)


schedule.every().day.at('14:00').do(job)

def expire():
    while True:
        schedule.run_pending()
        time.sleep(60)
