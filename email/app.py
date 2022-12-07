#!/usr/bin/env python3

import redis
import os
from datetime import datetime
import smtplib
import re
from email.mime.text import MIMEText

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_PASSWORD = ""
EMAIL_TO = os.environ.get('EMAIL_TEST_RECIPIENT')
SMTP_SERVER = os.environ.get('SMTP_SERVER')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_USERNAME = os.environ.get('EMAIL_USER')
SMTP_PASSWORD = os.environ.get('EMAIL_PASSWORD') 

MIN_MAG_TO_REPORT = 4.8

def email():
    try:
        red = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
        sub = red.pubsub()
        sub.subscribe('earthquakes')

        for message in sub.listen():
            if message is not None and isinstance(message, dict):
                msg = eval(str(message['data']))
                try:
                    title = msg["place"]
                    ts = msg["time"]
                    result = re.search(r".* ([\d.]+)", str(msg["mag"]))
                    mag = float(str(result.group(1)))
                    print(f"{ts}: {title} {mag}")
                    if(mag > MIN_MAG_TO_REPORT):
                        sendEmail(ts, title)
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)

def sendEmail(time, title):
    try:
        content=f"{time}: {title}"
        msg = MIMEText(content)
        msg['Subject'] = f"Earthquake Alert - {time}"
        msg['From'] = SMTP_USERNAME
        msg['To'] = EMAIL_TO
        mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        mail.starttls()
        mail.login(SMTP_USERNAME, SMTP_PASSWORD)
        mail.sendmail(SMTP_USERNAME, EMAIL_TO, msg.as_string())
        mail.quit()
        print ("Email sent successfully")

    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    while True:
        email()
