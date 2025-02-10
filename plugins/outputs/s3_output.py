# plugins/outputs/s3_output.py
import boto3
from ..metric import Metric

class S3OutputPlugin:
    def __init__(self, bucket: str, region: str = "us-east-1"):
        self.bucket = bucket
        self.client = boto3.client("s3", region_name=region)

    def write(self, metrics: list[Metric]):
        for metric in metrics:
            self.client.put_object(
                Bucket=self.bucket,
                Key=f"metrics/{metric.name}.json",
                Body=json.dumps(metric.__dict__),
            )