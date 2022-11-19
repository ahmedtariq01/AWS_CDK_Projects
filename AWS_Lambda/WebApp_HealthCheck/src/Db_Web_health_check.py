import boto3
import os

def lambda_handler(event, context):
    client = boto3.client('dynamodb', region_name='us-east-2')
    dbtable = os.environ('AlarmTable')
    table = client.Table(dbtable)
    message = event["Records"][0]["Sns"]["MessageId"]
    time = event["Records"][0]["Sns"]["Timestamp"]
    response = table.put_item(Item={"id": message, "timestamp": time})

