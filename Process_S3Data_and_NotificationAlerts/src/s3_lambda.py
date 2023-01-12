import boto3
import json
import os
import collections

# s3 client configuration
#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#client
s3 = boto3.client("s3")

# db client configuration
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#client
db = boto3.resource("dynamodb", region_name="us-east-2")

# sns client configuration
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#client
sns = boto3.client("sns")


def lambda_handler(event, context):
        
    # retrieves the source S3 bucket name and the key name of the uploaded object 
    # https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = str(event['Records'][0]['s3']['object']['key'])
    
    # getting the object from the bucket
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
    response = s3.get_object(Bucket=bucket, Key=key)
    
    # getting the object content
    data = response['Body'].read().decode('utf-8')
    
    word_counts = count_words(data)

    # Print the word counts
    for word, count in word_counts.items():
        print(f"{word}: {count}")
        
    db = boto3.resource("dynamodb", region_name="us-east-2")
    # https://www.geeksforgeeks.org/python-os-getenv-method/
    # Get key value of the table
    dbnameTable = os.environ["S3_Table"]
    table = db.Table(dbnameTable)
    
    # put item into the table
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.put_item
    # table.put_item(Item=word_counts, id=id)
    
    table.put_item(Item={"id": str(key), "Word_count": str(word_counts)})

    
    # create the SNS topic
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#topic
    # Set the target email address
    target_email = 'user@example.com'

    # Set the name of the SNS topic
    topic_name = 'ResultTopic'
    response = sns.create_topic(Name=topic_name)
    # set the ARN of the SNS topic
    topic_arn = "topic_arn"
    
    
    # Subscribe the email address to the SNS topic
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#subscription
    response = sns.subscribe(
              TopicArn=topic_arn,
              Protocol='email',
              Endpoint=target_email
)
    # Set the subject, and body of the email
    email_subject = 'Results of the World Count Process'
    email_body = 'The results of your World Count Process is: \n\n{}'.format(word_counts)
    response = sns.publish(
      Target=topic_arn,
      Message=email_body,
      Subject=email_subject,
)
    
    return word_counts
    

def count_words(filename):
      # Create a dictionary to store the word counts
  word_counts = collections.defaultdict(int)

  # Open the file for reading
  with open(filename, "r") as file:
    # Read the file line by line
    for line in file:
      # Split the line into words
      words = line.split()

      # Iterate over the words and count them
      for word in words:
        word_counts[word] += 1

  # Return the word counts
  return word_counts


    
    