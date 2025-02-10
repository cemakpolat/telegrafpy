# plugins/outputs/http_output.py
import requests
import json
from base import Metric, OutputPlugin

class HTTPOutputPlugin(OutputPlugin):
    def __init__(self, url: str):
        self.url = url

    def write(self, metrics: list[Metric]):
        try:
            # Convert metrics to JSON
            metrics_json = [metric.__dict__ for metric in metrics]

            # Send metrics to the HTTP endpoint
            response = requests.post(self.url, json=metrics_json)
            response.raise_for_status()  # Raise an exception for HTTP errors
        except Exception as e:
            print(f"Error sending metrics to HTTP endpoint: {e}")