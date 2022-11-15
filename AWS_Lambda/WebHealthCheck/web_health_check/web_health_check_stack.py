from aws_cdk import (
    Duration,
    aws_lambda as lambda_ ,
    aws_events as events_,
    aws_events_targets as targets_,
    Stack,
    RemovalPolicy,
)
from constructs import Construct

class WebHealthCheckStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # The code that defines your stack goes here
        fn = self.create_lambda('WebHealthCheck','./resources','web_health_check.lambda_handler')
        
        # destroy the lambda function when the stack is destroyed
        fn.apply_removal_policy(RemovalPolicy.DESTROY)
         
        # create a rule to trigger the lambda function every 60 minutes
        schedule=events_.Schedule.rate(Duration.minutes(60))
        
        # defines the target function
        targets=targets_.LambdaFunction(handler=fn)
        
        # corn job rule to trigger the lambda function
        rule = events_.Rule(self, "WebHealthRule",
            schedule = schedule,
            targets = targets
        )
 
        # destroy the rule when the stack is destroyed
        rule.apply_removal_policy(RemovalPolicy.DESTROY)

    # creating a lambda function
    def create_lambda(self, id, asset, handler):
        return lambda_.Function(self,
        id = id,
        handler = handler,
        code = lambda_.Code.from_asset(asset),
        runtime=lambda_.Runtime.PYTHON_3_9)

