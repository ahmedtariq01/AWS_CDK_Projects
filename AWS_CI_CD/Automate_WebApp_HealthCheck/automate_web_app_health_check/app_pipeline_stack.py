from aws_cdk import (
    Duration,
    aws_lambda as lambda_ ,
    aws_events as events_,
    aws_events_targets as targets_,
    Stack,
    RemovalPolicy,
    aws_cloudwatch as cloudwatch_,
    aws_iam as iam_,
    aws_sns as sns_,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as cw_actions_,
    aws_dynamodb as dynamodb_, 
    
)

from constructs import Construct
from src import constants as const


class AppPipelineStack(Stack):
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)