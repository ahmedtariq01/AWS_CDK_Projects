import aws_cdk as core
import aws_cdk.assertions as assertions

from automate_web_app_health_check.automate_web_app_health_check_stack import AutomateWebAppHealthCheckStack

# example tests. To run these tests, uncomment this file along with the example
# resource in automate_web_app_health_check/automate_web_app_health_check_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AutomateWebAppHealthCheckStack(app, "automate-web-app-health-check")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
