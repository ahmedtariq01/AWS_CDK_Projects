from aws_cdk import (
     Duration,
    aws_lambda as lambda_ ,
    aws_events as events_ ,
    aws_events_targets as targets_ ,
    aws_cloudwatch as cloudwatch_,
    Stack,
    RemovalPolicy,
    aws_iam as iam_,
    aws_sns as sns_,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as cw_actions_,
    aws_dynamodb as dynamodb_,
    aws_s3 as s3_,
    aws_s3_notifications as s3_notifications_,
    aws_apigateway as apigateway_,
)
from constructs import Construct

class UploadingLargePayloadsOnS3ThroughApiGatewayStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # lambda role
        lambda_role = self.create_lambda_role()
        
        fn = self.create_lambda('S3Lambda','./src','s3_files_lambda.lambda_handler',lambda_role)
        fn.apply_removal_policy(RemovalPolicy.DESTROY)
        
        apifn = self.create_lambda('APILambda','./src','presigned_url_lambda.lambda_handler',lambda_role)
        apifn.apply_removal_policy(RemovalPolicy.DESTROY)
        
        # creating a bucket
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_s3/Bucket.html
        bucket = s3_.Bucket(self, "MyBucket",
                            bucket_name="bucket_name",
                            versioned=True,
                            auto_delete_objects=False,
                            public_read_access=True                            
                            )
        bucket.apply_removal_policy(RemovalPolicy.DESTROY)
        
        # adding event notification to the bucket
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_s3_notifications/README.html
        bucket.add_event_notification(s3_.EventType.OBJECT_CREATED, s3_notifications_.LambdaDestination(fn))
        bucket.grant_read_write(fn)
        fn.add_environment("bucket_name", bucket.bucket_name)
        fn.grant_invoke(iam_.ServicePrincipal("s3.amazonaws.com"))
        
        # invoking the lambda function
        apifn.grant_invoke(iam_.ServicePrincipal("apigateway.amazonaws.com"))
        apifn.add_environment("bucket_name", bucket.bucket_name)
        apifn.grant_invoke(iam_.ServicePrincipal("s3.amazonaws.com"))
        
        # create REST API Gateway integrated with APILambda
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/LambdaRestApi.html
        api = apigateway_.LambdaRestApi(self, "api",
                rest_api_name ="PayLoadAPI",                        
                handler = apifn,
                proxy=False,
                endpoint_configuration= apigateway_.EndpointConfiguration(
                    types= [apigateway_.EndpointType.REGIONAL]
                )
            )
        
        # add resource and method
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/Resource.html
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/IResource.html#aws_cdk.aws_apigateway
        # path to resource
        api_method = api.root.add_resource("items")
        
        # POST: (Create) /items        
        api_method.add_method("POST")
    
        
        

    # creting a lambda function
    def create_lambda(self, id, asset, handler,role):
        return lambda_.Function(self,
            id = id,
            handler = handler,
            code = lambda_.Code.from_asset(asset),
            role = role,
            runtime=lambda_.Runtime.PYTHON_3_9,
            timeout=Duration.minutes(1))
            
            
    # creating a lambda role
    def create_lambda_role(self):
        lambdaRole = iam_.Role(self, "lambda-role",
            assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam_.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonSESFullAccess"),                
                
            ])
        return lambdaRole
        

        