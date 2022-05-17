import schedule
import time

def foo():
    print('helo')
    print(time.time())

schedule.every(3).seconds.do(foo)

while True:
    schedule.run_pending()
    time.sleep(1)