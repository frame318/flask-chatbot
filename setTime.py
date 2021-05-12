# import schedule
# import time
# import datetime
#
# def job():
#     print("Hello World")
#
# schedule.every().day.at("21:11").do(job)
#
# while True:
#     schedule.run_pending()
#     x = datetime.datetime.now()
#     y = x.strftime("%Y")
#     m = x.strftime("%m")
#     d = x.strftime("%d")
#     sum = y+'-'+m+'-'+d
#     print(sum)
#     time.sleep(1)


# import time
# import atexit
# from apscheduler.schedulers.background import BackgroundScheduler
# def print_time():
#     print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
# scheduler = BackgroundScheduler()
# scheduler.add_job(func=print_time, trigger="interval", seconds=3)
# scheduler.start()
# atexit.register(lambda: scheduler.shutdown())

import requests
import json
data = requests.get('https://covid19.th-stat.com/api/open/today')
json_data = json.loads(data.text)

Confirmed = json_data['Confirmed']  # ติดเชื้อสะสม
Recovered = json_data['Recovered']  # หายแล้ว
Hospitalized = json_data['Hospitalized']  # รักษาอยู่ใน รพ.
Deaths = json_data['Deaths']  # เสียชีวิต
NewConfirmed = json_data['NewConfirmed']
