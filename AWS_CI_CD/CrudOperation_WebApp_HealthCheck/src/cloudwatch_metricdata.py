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
    # Create and enable actions on an alarm in cloudwatch
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_alarm
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/cw-example-using-alarms.html?highlight=cloudwatch%20alarm
    def cloudWatch_metric_alarm (self ,AlarmName,AlarmActions,MetricName,namespace,dimensions,threshold,compop):
        response= self.client.put_metric_alarm(
            AlarmName = AlarmName,
            AlarmActions=AlarmActions,
            MetricName=MetricName,
            Namespace = namespace,
            Dimensions=dimensions,
            Threshold=threshold,
            ComparisonOperator=compop,
            Statistic = "Average",
            Period = 120,
            EvaluationPeriods = 1
        )
