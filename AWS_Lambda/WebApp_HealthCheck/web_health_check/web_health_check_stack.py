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
    
)
from constructs import Construct
from src import constants as const

class WebHealthCheckStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # lambda role
        lambda_role = self.create_lambda_role()
        
        # The code that defines your stack goes here
        fn = self.create_lambda('WebHealthCheck','./src','web_health_check.lambda_handler',lambda_role)
        
        # destroy the lambda function when the stack is destroyed
        fn.apply_removal_policy(RemovalPolicy.DESTROY)
         
        # create a rule to trigger the lambda function every 60 minutes
        schedule=events_.Schedule.rate(Duration.minutes(60))
        
        # defines the target function
        targets=targets_.LambdaFunction(handler=fn)
        
        # corn job rule to trigger the lambda function
        rule = events_.Rule(self, "WebHealthRule",
            description="Rule to generate the auto events for  Web Health Check",
            schedule = schedule,
            targets = [targets]
        )
 
        # destroy the rule when the stack is destroyed
        rule.apply_removal_policy(RemovalPolicy.DESTROY)
        
        # creating an SNS topic
        my_topic = sns_.Topic(self, "Health cHeck Notification")
        my_topic.add_subscription(subscriptions_.EmailSubscription("ahmed.tariq.skipq@gmail.com"))
        
        
        # creating the cloud Watch alarm for the availability metric
        dimensions = {'URls': str(url) for url in const.urls}
        
        avaiilability_metric = cloudwatch_.Metric(
            metric_name=const.availability_metric,
            namespace = const.namespace,
            dimensions_map= dimensions,
        )
        avaiilability_alarm =  cloudwatch_.Alarm(self, "Availability_Error",
            metric=avaiilability_metric,
            evaluation_periods=60,
            threshold=1,
            comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD, 
        
        )
        
        # adding the SNS action to the alarm
        avaiilability_alarm.add_alarm_action(cw_actions_.SnsAction(my_topic))
        
        
        # creating the cloud Watch alarm for the latency metric
        dimensions = {'URls': str(url) for url in const.urls}
        
        latency_metric = cloudwatch_.Metric(
            metric_name=const.latency_metric,
            namespace = const.namespace,
            dimensions_map= dimensions,
        )
        latency_alarm =  cloudwatch_.Alarm(self, "Latency_Errors",
            metric=latency_metric,
            evaluation_periods=60,
            threshold=0.5,
            comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD, 
        
        )
        
        # adding the SNS action to the alarm
        latency_alarm.add_alarm_action(cw_actions_.SnsAction(my_topic))
    

    # creating a lambda function
    def create_lambda(self, id, asset, handler, role):
        return lambda_.Function(self,
        id = id,
        handler = handler,
        code = lambda_.Code.from_asset(asset),
        runtime=lambda_.Runtime.PYTHON_3_9)

    # creating a lambda role
    def create_lambda_role(self):
        lambdaRole = iam_.Role(self, "Lambda_Role",
            assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
              iam_.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),  
              iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                
            ])
        return lambdaRole
    
    
    
    
    
    
    
    