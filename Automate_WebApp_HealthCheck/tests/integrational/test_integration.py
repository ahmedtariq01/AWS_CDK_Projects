# import aws_cdk as core
# import aws_cdk.assertions as assertions
# import pytest
# from aws_cdk import integ_tests
# from constructs import Construct
# from automate_web_app_health_check.automate_web_app_health_check_stack import AutomateWebAppHealthCheckStack




# def test_lambda_handler_name():
#     app = core.App()
#     stack = AutomateWebAppHealthCheckStack(app, "automate-web-app-health-check")
#     integ = integ_tests.IntegTest(app, "IntegTest",test_cases=[stack])
#     invoke = integ_tests.integ.assertions.invoke_function(function_name="web_health_check")
#     invoke.expect(integ_tests.ExpectedResult.object_like({
#                         "Payload": "200"
#                 }
#             )
#         )
    