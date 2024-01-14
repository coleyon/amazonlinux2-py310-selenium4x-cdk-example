import aws_cdk as cdk
from cdk_stacks.test_stack import SeleniumTestStack

app = cdk.App()
SeleniumTestStack(app, "SeleniumTestStack", env={"region": "us-east-1"})

app.synth()
