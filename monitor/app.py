#!/usr/bin/env python3

import redis
import json
import time
import feedparser
import re
from datetime import datetime

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_PASSWORD = ""

POLL_INTERVAL = 120

RSS_URL = "https://www.emsc-csem.org/service/rss/rss.php?typ=emsc"

def monitor():
    latest = datetime.strptime('1970-01-01 00:00:00 UTC','%Y-%m-%d %H:%M:%S %Z')
    try:
        r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

        while True:
            d = feedparser.parse(RSS_URL)
            for entry in reversed(d.entries):
                eq = {}
                result = re.search(r"[Mm][A-Z,a-z]? ....(.*)", entry.title.title())
                eq["place"] = str(result.group(1)).strip()
                eq["time"] = entry.emsc_time
                eq["lat"] = entry.geo_lat
                eq["long"] = entry.geo_long
                eq["depth"] = entry.emsc_depth
                result = re.search(r".* ([\d.]+)", entry.emsc_magnitude)
                eq["mag"] = str(result.group(1))
                eq["link"] = entry.link
                etime = datetime.strptime(entry.emsc_time,'%Y-%m-%d %H:%M:%S %Z')
                if etime > latest:
                    print(f"{eq['time']} - {eq['place']} - {eq['mag']}")
                    latest = etime
                    r.publish('earthquakes', json.dumps(eq)) 
            time.sleep(POLL_INTERVAL)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    while True:
        monitor()
