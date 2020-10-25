import schedule
import time

def job():
    print('Gamer time')
    
schedule.every(4).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
