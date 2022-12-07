import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest

from crud_operation_web_app_health_check.crud_operation_web_app_health_check_stack import CrudOperationWebAppHealthCheckStack

 
@pytest.fixture
def stack():
    app = core.App()
    stack = CrudOperationWebAppHealthCheckStack(app, "crud-operation-web-app-health-check")
    return stack

def test_dynamodb_exists(stack):
    db_table = stack.create_DynamoDB_table
    assert db_table is not None

def test_lambda_function_exists(stack):
    lambda_function = stack.create_lambda
    assert lambda_function is not None