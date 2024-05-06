#!/usr/bin/env python3

import redis
import json
import time
import requests
from datetime import datetime, timedelta

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_PASSWORD = ""

POLL_INTERVAL = 240
PREVIOUS_24_HOURS = 24*60*60

API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&orderby=time-asc&minmagnitude=3"

def monitor():
    guids = {}
    try:
        r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

        while True:
            url = API_URL
            fiveMinsAgo = datetime.utcnow() - timedelta(minutes=5)

            if len(guids) == 0:
                timeParams = "&updatedafter="+datetime.utcnow().strftime('%Y%m%dT000000')
            else:
                timeParams = "&updatedafter="+fiveMinsAgo.strftime('%Y%m%dT%H%M%S')

            url += timeParams
            response = requests.get(url)

            json_data = response.json() if response and response.status_code == 200 else None
            if json_data and 'features' in json_data:
                for feature in json_data['features']:
                    guid = feature['id']
                    ts = int(feature['properties']['time'])/1000
                    if guid not in guids and (ts+PREVIOUS_24_HOURS>=int(time.time())):
                        eq = {}
                        place = feature['properties']['place']
                        eq["place"] = place[0].upper() + place[1:]
                        eq["time"] = datetime.utcfromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S')
                        eq["lat"] = feature['geometry']['coordinates'][1]
                        eq["long"] = feature['geometry']['coordinates'][0]
                        eq["depth"] = feature['geometry']['coordinates'][2]
                        eq["mag"] = feature['properties']['mag']
                        eq["link"] = feature['properties']['url']
                        print(f"{eq['time']} - {eq['place']} - {eq['mag']}")
                        guids[guid] = True
                        r.publish('earthquakes', json.dumps(eq))
            time.sleep(POLL_INTERVAL)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    while True:
        monitor()
