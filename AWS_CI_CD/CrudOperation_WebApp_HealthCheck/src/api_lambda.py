import json
import os
import boto3

client = boto3.resource('dynamodb', region_name='us-east-2')
db_table = os.environ['APITable']
table = client.Table(db_table)

URL=[]

# Calling functions based on httpmethod and url path
def lambda_handler(event, context):
    httpmethod=event["httpMethod"]
    url=event["body"]
    
    # adding url to the table
    if httpmethod=="PUT":
        response = table.put_item(
                            Item={ 
                                "url":url
                            }
                        )
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': 'URL Added Successfully'
        }
        
    # read the url from the table
    if httpmethod=="GET":
        response = table.scan()
        data=response["Items"]
        for urls in data:
            URL.append(urls['url'])
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': URL
        }
        
    # update the url from the table
    if httpmethod=="PATCH":
        url = data["id"]
        url_data = data["url_name"]
        updateKey = "website"
        response = table.update_item(
            Key={"id": url},
            UpdateExpression="SET %s = :newURL" % updateKey,
            ExpressionAttributeValues={":newURL": url_data},
            ExpressionAttributeNames={"#u": "URL"},
        )
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': 'URL Updated Successfully'
        }

    # delete the url from the table
    if httpmethod=="DELETE":
        response=table.delete_item(
                            Key={
                                "url":url
                                }
                        )
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': 'URL Deleted Successfully'
        }






