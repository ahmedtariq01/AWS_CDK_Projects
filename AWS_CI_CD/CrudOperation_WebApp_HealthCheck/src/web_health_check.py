import urllib3
import datetime
from cloudwatch_metricdata import AWSCloudWatch
import constants as const
import constants as const
import boto3
import os

# https://dynobase.dev/dynamodb-python-with-boto3/#list-tables
db = boto3.resource('dynamodb', region_name='us-east-2')

# https://www.geeksforgeeks.org/python-os-environ-object/
# Get key value of the table
dbnameTable=os.environ["APITable"]
table=db.Table(dbnameTable)
# Get topic of sns
snsTopic=os.environ["snsTopic"]
AlarmActions = ["arn:aws:sns:us-east-2:315997497220:{snsTopic}".format(snsTopic=snsTopic)]

#array for storing websites
URL =[]
#Executing Functions to fetch website active status and latency
values=[]

# lambda_handler is the entry point for AWS Lambda. Check 4 URLs and return the results
def lambda_handler(event, context):
    # creating cloudwatch object to put the metric data
    cloudwatch_obj = AWSCloudWatch()
    
    #values extraction from table using scan
    response = table.scan()
    lists=response["Items"]
    for urls in lists:
        URL.append(urls['url'])
    
    # check the availability and latency of the URLs
    for url in const.urls:
        availability=getAvailability(url)
        latency=getLatency(url)        
        
        # sending the metric data to AWS CloudWatch
        dimensions = [{'Name': 'URls', 'Value': url}]
        cloudwatch_obj.cloudwatch_metric_data(const.namespace, const.availability_metric, dimensions, availability)
        cloudwatch_obj.cloudWatch_metric_alarm("Availability of "+str(url),
        AlarmActions,const.availability_metric,const.namespace,dimensions,1,"LessThanThreshold")
        
        cloudwatch_obj.cloudwatch_metric_data(const.namespace, const.latency_metric, dimensions, latency)
        cloudwatch_obj.cloudWatch_metric_alarm("Layency of "+str(url),
        AlarmActions,const.latency_metric,const.namespace,dimensions,1,"LessThanThreshold")
        
        # values.update({'availability': availability, 'latency': latency})
        values.append({ "Availability: "+ str(url) : availability , "Latency: "+str(url) : latency})
        
    return values

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
    
    
    