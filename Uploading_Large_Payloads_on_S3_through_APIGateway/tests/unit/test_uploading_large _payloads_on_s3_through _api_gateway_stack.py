import aws_cdk as core
import aws_cdk.assertions as assertions

from uploading_large _payloads_on_s3_through _api_gateway.uploading_large _payloads_on_s3_through _api_gateway_stack import UploadingLargePayloadsOnS3ThroughApiGatewayStack

# example tests. To run these tests, uncomment this file along with the example
# resource in uploading_large _payloads_on_s3_through _api_gateway/uploading_large _payloads_on_s3_through _api_gateway_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = UploadingLargePayloadsOnS3ThroughApiGatewayStack(app, "uploading-large--payloads-on-s3-through--api-gateway")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
