url = 'www.google.com'

import urllib3
import datetime

def lambda_handler(event, context):
    values = dict()
    availability = getAvailability()
    latency = getLatency()
    values.update({'availability': availability, 'latency': latency})
    return values

def getAvailability():
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    if response.status == 200:
        return 1.0
    else:
        return 0.0
    
def getLatency():
    http = urllib3.PoolManager()
    start = datetime.datetime.now()
    response = http.request('GET', url)
    response = http.request('GET', url)
    end = datetime.datetime.now()
    latency = round((end - start).microseconds * .000001,6)
    return latency
