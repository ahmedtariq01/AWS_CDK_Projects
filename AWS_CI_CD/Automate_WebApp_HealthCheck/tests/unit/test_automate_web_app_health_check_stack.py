import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest

from automate_web_app_health_check.automate_web_app_health_check_stack import AutomateWebAppHealthCheckStack

 
@pytest.fixture
def app():
    app = core.App()
    return app


# code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
# check wheteher lambda is created or not
def test_lambda(app):
    app = app
    stack = AutomateWebAppHealthCheckStack(app, "automate-web-app-health-check")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::Lambda::Function", 2)
   
    
# Check whether SNS is created or not
def test_sns(app):
    app = app
    stack = AutomateWebAppHealthCheckStack(app, "automate-web-app-health-check")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::SNS::Topic", 1)
    
# check the lambda handler function name
def test_lambda_handler(app):
    app = app
    stack = AutomateWebAppHealthCheckStack(app, "automate-web-app-health-check")
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties("AWS::Lambda::Function", {
        "Handler": "web_health_check.lambda_handler",
        "Handler": "Db_Web_health_check.lambda_handler"
    })

# Check whether DB table is created or not 
def test_dynamodb(app):
    app = app
    stack = AutomateWebAppHealthCheckStack(app, "automate-web-app-health-check")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::DynamoDB::Table", 1)
    
# check the number of alarms created in CloudWatch
def test_cloudwatch(app):
    app = app
    stack = AutomateWebAppHealthCheckStack(app, "automate-web-app-health-check")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::CloudWatch::Alarm", 4)

# check the SNS subscriptions email
def test_SNS_Subscription(app):
    app = app
    stack = AutomateWebAppHealthCheckStack(app, "automate-web-app-health-check")
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties("AWS::SNS::Subscription", {
        "Endpoint": "test@example.com"
    })
    
# check the number of rules created in CloudWatch
def test_cloudwatch_rule(app):
    app = app
    stack = AutomateWebAppHealthCheckStack(app, "automate-web-app-health-check")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::Events::Rule", 1)
    
# check the IAM role created for lambda
def test_lambda_role(app):
    app = app
    stack = AutomateWebAppHealthCheckStack(app, "automate-web-app-health-check")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::IAM::Role", 1)
    
# check the IAM policies created for lambda
def test_lambda_policy(app):
    app = app
    stack = AutomateWebAppHealthCheckStack(app, "automate-web-app-health-check")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::IAM::Policy", 2)
    
# check the cloudwatch metrics
def test_cloudwatch_metrics(app):
    app = app
    stack = AutomateWebAppHealthCheckStack(app, "automate-web-app-health-check")
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties("AWS::CloudWatch::Alarm", {
        "MetricName": "URL_AVAILABILITY",
        "MetricName": "URL_LATENCY"
    })
    
# functional test to check the lambda handler function name
# def test_lambda_handler_function():
#     app = core.App()
#     stack = AutomateWebAppHealthCheckStack(app, "automate-web-app-health-check")
#     lambda_handler = stack.lambda_handler
#     assert lambda_handler is not None
#     assert lambda_handler.function_name == "web_health_check"
#   assert lambda_handler.runtime == lambda_.Runtime.PYTHON_3_8