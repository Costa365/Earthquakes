#!/usr/bin/env python3

import redis
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_PASSWORD = ""
EMAIL_TO = os.environ.get('EMAIL_TEST_RECIPIENT')
SMTP_SERVER = os.environ.get('SMTP_SERVER')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_USERNAME = os.environ.get('EMAIL_USER')
SMTP_PASSWORD = os.environ.get('EMAIL_PASSWORD') 

MIN_MAG_TO_REPORT = 5.8

def email():
    try:
        red = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)
        sub = red.pubsub()
        sub.subscribe('earthquakes')

        for message in sub.listen():
            if message is not None and isinstance(message, dict) and message['type']=='message':
                msg = eval(str(message['data']))
                try:
                    mag = float(str(msg["mag"]))
                    if(mag > MIN_MAG_TO_REPORT):
                        mime = prepareEmail(msg)
                        if mime != None:
                            sendEmail(mime)     
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)

def prepareContent(msg):
    content = ""
    try:
        content = f"Earthquake Alert\n\n"
        content += f"Time: {msg['time']}\n"
        content += f"Place: {msg['place']}\n"
        content += f"Magnitude: {msg['mag']}\n"
        content += f"Depth: {msg['depth']}km\n"
        content += f"More information: {msg['link']}\n"
    except Exception as e:
        print(e)
    finally:
        return content

def prepareEmail(msg):
    try:
        content=prepareContent(msg)
        place = msg["place"]
	mag = msg["mag"]
        mime = MIMEText(content)
        mime['Subject'] = f"Earthquake Alert - {place} - {mag}"
        mime['From'] = SMTP_USERNAME
        mime['To'] = EMAIL_TO
        return mime
    except Exception as e:
        print(e)
        return None

def sendEmail(mime):
    try:
        mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        mail.starttls()
        mail.login(SMTP_USERNAME, SMTP_PASSWORD)
        mail.sendmail(SMTP_USERNAME, EMAIL_TO, mime.as_string())
        mail.quit()
        print (f"{mime['Subject']} - Email sent successfully")
    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    while True:
        email()
