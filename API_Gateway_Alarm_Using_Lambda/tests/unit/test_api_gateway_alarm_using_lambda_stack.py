import aws_cdk as core
import aws_cdk.assertions as assertions

from api_gateway_alarm_using_lambda.api_gateway_alarm_using_lambda_stack import ApiGatewayAlarmUsingLambdaStack

# example tests. To run these tests, uncomment this file along with the example
# resource in api_gateway_alarm_using_lambda/api_gateway_alarm_using_lambda_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ApiGatewayAlarmUsingLambdaStack(app, "api-gateway-alarm-using-lambda")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
