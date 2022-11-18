import urllib3
import datetime
import json
from cloudwatch_metricdata import AWSCloudWatch
import constants as const

# lambda_handler is the entry point for AWS Lambda. Check 4 URLs and return the results
def lambda_handler(event, context):
    # creating cloudwatch object to put the metric data
    cloudwatch_obj = AWSCloudWatch()
    values = dict()
    
    # check the availability and latency of the URLs
    for url in const.urls:
        availability=getAvailability(url)
        latency=getLatency(url)        
        
        # sending the metric data to AWS CloudWatch
        dimensions = [{'Name': 'URls', 'Value': const.urls}]
        cloudwatch_obj.cloudwatch_metric_data(const.namespace, const.availability_metric, dimensions, availability)
        cloudwatch_obj.cloudwatch_metric_data(const.namespace, const.latency_metric, dimensions, latency)
        values.update({'availability': availability, 'latency': latency})
         # values.update({ "Availability"+ str(url) : availability , "Latency"+str(url) : latency})
        
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
    
    
    