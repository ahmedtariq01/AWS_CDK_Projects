#!/usr/bin/env python3

import aws_cdk as cdk

from hello_world.hello_world_stack import HelloWorldStack


app = cdk.App()
HelloWorldStack(app, "hello-world",
    env=cdk.Environment(account='123456789', region='us-east-2'),)

app.synth()
