import json
import boto3
from pprint import pprint
from datetime import datetime

logGroupName='logGroupName'
values = {"Operations":[]}
summary=[]
def lambda_handler(event, context):
    #Extract CloudWatch Logs
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.get_log_events
    client = boto3.client('logs')
    response = client.get_log_events(
        logGroupName='logGroupName',
        logStreamName='logStreamName',
    )
    data = response
    val=list(data.values())
    #Adding to Dictionary
    # https://careerkarma.com/blog/python-add-to-dictionary
    for i in range(len(val[0])):
        time = (val[0][i]['timestamp'])
        #Converting Timestamp 
        # https://pynative.com/python-timestamp/
        dt = datetime.fromtimestamp(time/ 1000)
        msg = (val[0][i]['message'])
        op = [dt,msg]
        values["Operations"].append(op)
    # print(arr)
    pprint(values)
    #Number of Operations
    numberOp=(len(values["Operations"]))
    ATdata = json.dumps(data)
    #Number of Success
    totals = ATdata.count("SUCCEEDED")
    print(totals)
    #Number of Warnings
    totalw = ATdata.count("WARNING")
    print(totalw)
    #Number of Passes
    totalp = ATdata.count("passed")
    print(totalp)
    sum = "Summary"+" "+"Operations:"+str(numberOp)+" "+"SUCCEEDED:"+str(totals)+" "+"WARNINGS:"+str(totalw)+" "+"Passed:"+str(totalp)
    summary.append(sum)
    
    #Verify Email First time only
    # # https://www.learnaws.org/2020/12/18/aws-ses-boto3-guide/
    ses_client = boto3.client("ses", region_name="us-east-2")
    response = ses_client.verify_email_identity(
        EmailAddress="user@example.com"
    )
    print(response)
    
    # Send File Data to Email
    #https://www.learnaws.org/2020/12/18/aws-ses-boto3-guide/
    ses_client = boto3.client("ses", region_name="us-east-2")
    CHARSET = "UTF-8"
    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "user@example.com",
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": str(summary),
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": json.dumps("Operations "+ str(logGroupName)),
            },
        },
        Source="user@example.com",
    )

    # Send File Data to Email
    #https://www.learnaws.org/2020/12/18/aws-ses-boto3-guide/
    ses_client = boto3.client("ses", region_name="us-east-2")
    CHARSET = "UTF-8"
    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "user@example.com",
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": str(values),
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": json.dumps("Operations "+ str(logGroupName)),
            },
        },
        Source="example@gmail.com",
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Success Data Sent!')
    }