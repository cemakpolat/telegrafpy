# plugins/outputs/prometheus_output.py
from prometheus_client import start_http_server, Gauge
from ..metric import Metric

class PrometheusOutputPlugin:
    def __init__(self, port: int = 8000):
        self.port = port
        self.gauges = {}
        start_http_server(self.port)

    def write(self, metrics: list[Metric]):
        for metric in metrics:
            if metric.name not in self.gauges:
                self.gauges[metric.name] = Gauge(metric.name, "", list(metric.tags.keys()))
            self.gauges[metric.name].labels(**metric.tags).set(metric.fields["value"])