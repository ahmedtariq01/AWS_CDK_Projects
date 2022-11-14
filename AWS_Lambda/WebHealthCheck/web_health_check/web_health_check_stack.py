from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_,
)
from constructs import Construct

class WebHealthCheckStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        fn = self.create_lambda('WebHealthCheck','./resources','web_health_check.lambda_handler')

    def create_lambda(self, id, asset, handler):
        return lambda_.Function(self,
        id = id,
        handler = handler,
        code = lambda_.Code.from_asset(asset),
        runtime=lambda_.Runtime.PYTHON_3_9)

