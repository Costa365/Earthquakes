#!/usr/bin/env python3

import redis
import json
import urllib.request
import time
import feedparser
from datetime import datetime

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_PASSWORD = ""

POLL_INTERVAL = 120

def monitor():
    latest = datetime.strptime('1970-01-01 00:00:00 UTC','%Y-%m-%d %H:%M:%S %Z')
    try:
        r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

        while True:
            d = feedparser.parse('https://www.emsc-csem.org/service/rss/rss.php?typ=emsc')
            for entry in reversed(d.entries):
                eq = {}
                eq["place"] = entry.title.title()
                etime = datetime.strptime(entry.emsc_time,'%Y-%m-%d %H:%M:%S %Z')
                eq["time"] = entry.emsc_time
                eq["lat"] = entry.geo_lat
                eq["long"] = entry.geo_long
                eq["depth"] = entry.emsc_depth
                eq["mag"] = entry.emsc_magnitude
                eq["link"] = entry.link
                if etime > latest:
                    print(eq["place"])
                    latest = etime
                    r.publish('earthquakes', json.dumps(eq)) 
            time.sleep(POLL_INTERVAL)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    while True:
        monitor()
