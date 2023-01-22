from aws_cdk import (
    aws_lambda as lambda_ ,
    RemovalPolicy,
    Duration,
    Stack,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_iam as iam_,
    
)
from constructs import Construct

class ApplicationNotificationSystemStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # lambda role
        lambda_role = self.create_lambda_role()
        
        # The code that defines your stack goes here
        fn = self.create_lambda('NotificationSystem','./src','app_notification.lambda_handler',lambda_role)
        fn.apply_removal_policy(RemovalPolicy.DESTROY)
        
        # create a rule to trigger the lambda function every 60 minutes
        schedule=events_.Schedule.rate(Duration.minutes(60))
        
        # defines the target function
        targets=targets_.LambdaFunction(handler=fn)
        
        # corn job rule to trigger the lambda function
        rule = events_.Rule(self, "NotificationRule",
            schedule = schedule,
            targets = [targets]
        )
        
        # destroy the rule when the stack is destroyed
        rule.apply_removal_policy(RemovalPolicy.DESTROY)
 
   
        
    # creating a lambda function
    def create_lambda(self, id, asset, handler, role):
        return lambda_.Function(self,
        id = id,
        handler = handler,
        code = lambda_.Code.from_asset(asset),
        role = role,
        runtime=lambda_.Runtime.PYTHON_3_9,
        timeout=Duration.minutes(1))
        
     # creating a lambda role
    def create_lambda_role(self):
        lambdaRole = iam_.Role(self, "Lambda_Role",
            assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[  
                iam_.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                iam_.ManagedPolicy.from_aws_managed_policy_name('AmazonSESFullAccess'),

              
            ]
        )
        return lambdaRole