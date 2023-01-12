import aws_cdk as core
import aws_cdk.assertions as assertions

from process_s3_data_and_notification_alerts.process_s3_data_and_notification_alerts_stack import ProcessS3DataAndNotificationAlertsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in process_s3_data_and_notification_alerts/process_s3_data_and_notification_alerts_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ProcessS3DataAndNotificationAlertsStack(app, "process-s3-data-and-notification-alerts")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
