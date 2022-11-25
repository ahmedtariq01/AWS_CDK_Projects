from aws_cdk import (
    Stage,
)

from automate_web_app_health_check.automate_web_app_health_check_stack import AutomateWebAppHealthCheckStack 
from constructs import Construct
from src import constants as const


class AppPipelineStage(Stage):
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        self.stage = AutomateWebAppHealthCheckStack(self, "AppPipelineStage")