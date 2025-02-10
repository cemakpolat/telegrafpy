# plugins/inputs/prometheus_input.py
import requests
from ..metric import Metric

class PrometheusInputPlugin:
    def __init__(self, url: str):
        self.url = url

    def gather(self) -> list[Metric]:
        response = requests.get(self.url)
        response.raise_for_status()
        data = response.json()
        metrics = []
        for result in data["data"]["result"]:
            metrics.append(
                Metric(
                    name="prometheus",
                    tags=result["metric"],
                    fields={"value": float(result["value"][1])},
                )
            )
        return metrics