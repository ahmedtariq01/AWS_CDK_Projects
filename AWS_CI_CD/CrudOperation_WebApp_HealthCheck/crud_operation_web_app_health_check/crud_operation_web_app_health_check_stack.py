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
    aws_codedeploy as codedeploy_,
    aws_apigateway as apigateway_,
)

from constructs import Construct
from src import constants as const

class CrudOperationWebAppHealthCheckStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # lambda role
        lambda_role = self.create_lambda_role()
        
        # The code that defines your stack goes here
        fn = self.create_lambda('WebHealthCheck','./src','web_health_check.lambda_handler',lambda_role)
        
        # DaynamoDB lambda function
        db = self.create_lambda('DbLambda','./src','Db_Web_health_check.lambda_handler',lambda_role)
        
        # Api lambda function
        apifn = self.create_lambda('APILambda','./src','api_lambda.lambda_handler',lambda_role)
        

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
        my_topic.add_subscription(subscriptions_.EmailSubscription("test@example.com"))
        
        
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
        
        # code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Function.html
        # obtaining metrics from aws
        # obtaining Duration metric
        duration_metric = fn.metric_duration()
        duration_alarm =  cloudwatch_.Alarm(self,"Duration_Error",
            metric=duration_metric,
            evaluation_periods=60,
            threshold=1,
            datapoints_to_alarm=60,
            comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD, 
            treat_missing_data=cloudwatch_.TreatMissingData.NOT_BREACHING
        
        )
        
        # obtaining invocations metric
        invocations_metric = fn.metric_invocations()
        invocations_alarm =  cloudwatch_.Alarm(self,"Invocations_Error",
            metric=invocations_metric,
            evaluation_periods=60,
            threshold=1,
            datapoints_to_alarm=60,
            comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD, 
            treat_missing_data=cloudwatch_.TreatMissingData.NOT_BREACHING
        )
        
        # code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_lambda/Alias.html#aws_cdk.aws_lambda.Alias
        # version of the application
        version = fn.current_version
        alias = lambda_.Alias(self, "WebAppHealthCheckAlias",
            alias_name="Prod",
            version=version
        )
        
        # code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/LambdaDeploymentGroup.html
        # code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/ILambdaDeploymentConfig.html#aws_cdk.aws_codedeploy.ILambdaDeploymentConfig
        # deployment group to Configure auto rollback if any of the metrics are in alarm
        deployment_group = codedeploy_.LambdaDeploymentGroup(self, "BlueGreenDeployment",
            alias=alias,
            alarms=[duration_alarm,invocations_alarm],
        # code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/AutoRollbackConfig.html#aws_cdk.aws_codedeploy.AutoRollbackConfig
            auto_rollback=codedeploy_.AutoRollbackConfig(  
                                        failed_deployment=True,
                                        stopped_deployment=True,
                                        deployment_in_alarm=True
            ),
                
        # code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/LambdaDeploymentConfig.html
            deployment_config=codedeploy_.LambdaDeploymentConfig.CANARY_10_PERCENT_10_MINUTES
        )
        
        # Calling the DynamoDB table
        db_table = self.create_DynamoDB_table()
        # db_table.grant_read_write_data(db)
        db_table.grant_full_access(db)
        db.add_environment("AlarmTable", db_table.table_name)
        my_topic.add_subscription(subscriptions_.LambdaSubscription(db))
        
        
        # Calling the API DynamoDB table
        API_table = dynamodb_.Table(self, "APITable",
        partition_key=dynamodb_.Attribute(name="id", type=dynamodb_.AttributeType.STRING))
        API_table.grant_full_access(apifn)
        apifn.add_environment("ApITable", API_table.table_name)
        
        # invoking the lambda function
        apifn.grant_invoke(iam_.ServicePrincipal("apigateway.amazonaws.com"))
        
        # create REST API Gateway integrated with APILambda
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/LambdaRestApi.html
        api = apigateway_.LambdaRestApi(self, id = "AhmedTariqAPI",
                handler = apifn,
                proxy=False,
                endpoint_configuration= apigateway_.EndpointConfiguration(
                    types= [apigateway_.EndpointType.REGIONAL]
                )
            )
        
        # add resource and method
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/Resource.html
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/IResource.html#aws_cdk.aws_apigateway
        # path to resource
        api_method = api.root.add_resource("items")
        
        # POST: (Create) /items        
        api_method.add_method("POST")
        
        # GET: (Read) /items
        api_method.add_method("GET")
        
        # DELETE: /items
        api_method.add_method("DELETE")
        
        #PUT: (Update) /items
        api_method.add_method("PATCH")
        

        
                                   
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
                iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
              
            ]
        )
        return lambdaRole
    
    # creating a DynamoDB table
    def create_DynamoDB_table(self):
        table = dynamodb_.Table(self, "AlarmTable",
        partition_key=dynamodb_.Attribute(name="id", type=dynamodb_.AttributeType.STRING),
        sort_key=dynamodb_.Attribute(name="timestamp", type=dynamodb_.AttributeType.STRING),
        removal_policy=RemovalPolicy.DESTROY
        )
        return table   

        





