from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lambda as lambda_,
    RemovalPolicy,
)


class HelloWorldStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # The code that defines your stack goes here
        fn = self.create_lambda('HelloLambda','./resources','hello_lambda.lambda_handler')
        
        # destroy the lambda function when the stack is destroyed
        fn.apply_removal_policy(RemovalPolicy.DESTROY)
    
    # creating a lambda function
    def create_lambda(self, id, asset, handler):
        return lambda_.Function(self,
            id = id,
            handler = handler,
            code = lambda_.Code.from_asset(asset),
            runtime=lambda_.Runtime.PYTHON_3_9)
