import aws_cdk as core
import aws_cdk.assertions as assertions

from application_notification_system.application_notification_system_stack import ApplicationNotificationSystemStack

# example tests. To run these tests, uncomment this file along with the example
# resource in application_notification_system/application_notification_system_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ApplicationNotificationSystemStack(app, "application-notification-system")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
