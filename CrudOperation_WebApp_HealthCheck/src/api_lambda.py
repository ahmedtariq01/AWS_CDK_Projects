import json
import os
import boto3

# https://dynobase.dev/dynamodb-python-with-boto3/#list-tables
db = boto3.resource('dynamodb', region_name='us-east-2')
        
#https://www.geeksforgeeks.org/python-os-getenv-method/
# Get key value of the table
dbnameTable=os.getenv("APITable")
table=db.Table(dbnameTable)

URL=[]
def lambda_handler(event, context):
    # Get the method
    httpmethod=event["httpMethod"]
    # Get the url
    url=event["body"]

    # Perform CRUD operation if method matches
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html?highlight=dynamodb
    if httpmethod=="POST":
        response = table.put_item(
                            Item={ 
                                "url":url
                            }
                        )
        # Return these lines to be shown in API when doing CRUD operation
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': 'URL Added Successfully'
        }
        
    
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
                'body': json.dumps(URL),
            }
      

    
    if httpmethod=="PATCH":
        response=table.update_item(
                            Key={
                                "url":url
                            },
                            UpdateExpression='SET url = :url11',
                            ExpressionAttributeValues={
                                                    ':url1': url
                                                    }
                            )
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': 'URL Updated Successfully'
        }
    
    if httpmethod=="DELETE":
        response=table.delete_item(
                                Key={
                                    "url":url
                                    }
                            )
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': 'URL Deleted Successfully'
        }
        
    
    
    