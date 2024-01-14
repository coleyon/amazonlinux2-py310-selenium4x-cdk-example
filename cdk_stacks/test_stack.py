from aws_cdk import Duration, Stack
from aws_cdk import aws_lambda as _lambda
from constructs import Construct

LAMBDA_TIMEOUT = 60


class SeleniumTestStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """Stack定義"""
        super().__init__(scope, construct_id, **kwargs)

        # Lambda Handler Definitions
        local_debug_lambda_handler = _lambda.DockerImageCode.from_image_asset(
            directory=".",
            cmd=["local_debug.handler"],
            file="local_debug.Dockerfile",
        )
        # Lambda Function Definitions
        _lambda.DockerImageFunction(
            scope=self,
            id="SeleniumTest",
            code=local_debug_lambda_handler,
            timeout=Duration.seconds(120),
            memory_size=1024,
            retry_attempts=0,
            description="sample lambda function for selenium test",
            environment={"APP_NAME": "web-crawler"},
        )
