import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest

from automate_web_app_health_check.automate_web_app_health_check_stack import AutomateWebAppHealthCheckStack

 
@pytest.fixture
def stack():
    app = core.App()
    stack = AutomateWebAppHealthCheckStack(app, "automate-web-app-health-check")
    return stack

def test_dynamodb_exists(stack):
    db_table = stack.create_DynamoDB_table
    assert db_table is not None

def test_lambda_function_exists(stack):
    lambda_function = stack.create_lambda
    assert lambda_function is not None