import boto3
import os
import json

# s3 client configuration
#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#client
s3 = boto3.client("s3")

# Getting bucket name
bucket =   os.environ['bucket_name']

def lambda_handler(event, context):
    # retrieves the source S3 bucket name and the key name of the uploaded object
    # https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html
    httpmethod=event["httpMethod"]
    if httpmethod=="POST":
        queryStringParameters = event["queryStringParameters"]
        file_name= queryStringParameters["file_name"]
        expiration = 60 * 60 * 24 # 24 hours
        signed_url = s3.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': bucket,
            'Key': file_name
        },
        ExpiresIn=expiration
    )
        return {
            'statusCode': 200,
            'body': json.dumps(signed_url)
        }

                

