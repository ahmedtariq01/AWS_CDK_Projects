import urllib3
import datetime
import json

urls = ['www.skipq.org', 'www.google.com', 'www.umt.edu.pk', 'www.amazon.com']

# lamda_handler is the entry point for AWS Lambda. Check 4 URLs and return the results
def lambda_handler(event, context):
    values = dict()
    availability = []
    latency = []
    for url in urls:
        availability.append(getAvailability(url))
        latency.append(getLatency(url))
    values.update({'availability': availability, 'latency': latency})
    return json.dumps(values, default=str)

# getAvailability returns the availability of a URL
def getAvailability(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    if response.status == 200:
        return 1.0
    else:
        return 0.0
    
# getLatency returns the latency of a URL
def getLatency(url):
    http = urllib3.PoolManager()
    start = datetime.datetime.now()
    response = http.request('GET', url)
    end = datetime.datetime.now()
    latency = round((end - start).microseconds * .000001,6)
    return latency
    