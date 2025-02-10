# plugins/outputs/slack_output.py
import requests
from ..metric import Metric

class SlackOutputPlugin:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def write(self, metrics: list[Metric]):
        for metric in metrics:
            message = {
                "text": f"Metric: {metric.name}\nTags: {metric.tags}\nFields: {metric.fields}"
            }
            requests.post(self.webhook_url, json=message)