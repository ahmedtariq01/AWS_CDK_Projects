import boto3


# class AWS_DYNAMODB:
#     def __init__(self) -> None:
#         self.client = boto3.client('dynamodb')
    
# lambda_handler is the entry point for AWS Lambda. Check 4 URLs and return the results
def lambda_handler( event, context):
    client = boto3.client('dynamodb')
    response = client.create_table(
    AttributeDefinitions=[
        {
            'AttributeName': 'string',
            'AttributeType': 'S'|'N'|'B'
        },
    ],
    TableName='string',
    KeySchema=[
        {
            'AttributeName': 'string',
            'KeyType': 'HASH'|'RANGE'
        },
    ],)
        
        
