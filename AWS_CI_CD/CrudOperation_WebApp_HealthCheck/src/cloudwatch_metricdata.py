import boto3

class AWSCloudWatch:
    def __init__(self) -> None:
        self.client = boto3.client('cloudwatch')

    # putMetricData puts the metric data to AWS CloudWatch
    def cloudwatch_metric_data(self, nampespace, metric_name, dimensions, value):
        response = self.client.put_metric_data(
                Namespace=nampespace,
                MetricData=[
                {
                    'MetricName': metric_name,
                    'Dimensions': dimensions,
                    'Value': value,    
                },
            ]
        )
        