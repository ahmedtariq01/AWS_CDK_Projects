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
        
        fn = self.create_lambda('WebHealthCheck','./resources','web_health_check.lambda_handler')
        
        fn.apply_removal_policy(RemovalPolicy.DESTROY)
         
        schedule=events_.Schedule.rate(Duration.minutes(60))
        
        targets=targets_.LambdaFunction(handler=fn)
        
        rule = events_.Rule(self, "WebHealthRule",
            schedule = schedule,
            targets = targets
        )

        rule.apply_removal_policy(RemovalPolicy.DESTROY)

    def create_lambda(self, id, asset, handler):
        return lambda_.Function(self,
        id = id,
        handler = handler,
        code = lambda_.Code.from_asset(asset),
        runtime=lambda_.Runtime.PYTHON_3_9)

