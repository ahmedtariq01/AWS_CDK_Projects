from aws_cdk import (
    Duration,
    aws_lambda as lambda_ ,
    aws_events as events_,
    aws_events_targets as targets_,
    Stage,
    RemovalPolicy,
    aws_cloudwatch as cloudwatch_,
    aws_iam as iam_,
    aws_sns as sns_,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as cw_actions_,
    aws_dynamodb as dynamodb_, 
    
)

from automate_web_app_health_check.automate_web_app_health_check_stack import AutomateWebAppHealthCheckStack 
from constructs import Construct
from src import constants as const


class AppPipelineStage(Stage):
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        self.stage = AutomateWebAppHealthCheckStack(self, "AppPipelineStage")