from aws_cdk import (
    Stage,
)

from crud_operation_web_app_health_check.crud_operation_web_app_health_check_stack import CrudOperationWebAppHealthCheckStack

from constructs import Construct
from src import constants as const


class AppPipelineStage(Stage):
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        self.stage = CrudOperationWebAppHealthCheckStack(self, "AppPipelineStage")