import boto3


# s3 client configuration
#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#client
s3 = boto3.client("s3")

# ses client configuration
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses.html#client
ses = boto3.client('ses', region_name='us-east-2')

def lambda_handler(event, context):
    # retrieves the source S3 bucket name and the key name of the uploaded object and the file data
    # https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html
    bucket = event['Records'][0]['s3']['bucket']['name']
    # bucket_data = event['body'] Body=bucket_data
    key = event['Records'][0]['s3']['object']['key']


    
    # Set the email address of the recipient
    to_email = 'example@gmail.com'

    # Set the email subject and body
    subject = 'A new file has been uploaded to the bucket'
    body = 'A new file has been uploaded to the bucket: ' + bucket + ' with the key: ' + key
    
    response = ses.send_email(
                        Source=to_email, 
                        Destination={'ToAddresses': [to_email]},
                        Message={
                        'Subject': {'Data': subject},
                        'Body': {'Text': {'Data': body}}
    })

    # Return a success response
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': 'File uploaded successfully and email sent to the user'
    }
