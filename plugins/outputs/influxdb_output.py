# plugins/outputs/influxdb_output.py
from influxdb import InfluxDBClient
from ..metric import Metric

class InfluxDBOutputPlugin:
    def __init__(self, host: str, port: int, database: str):
        self.client = InfluxDBClient(host=host, port=port, database=database)

    def write(self, metrics: list[Metric]):
        points = [
            {
                "measurement": metric.name,
                "tags": metric.tags,
                "fields": metric.fields,
                "time": metric.timestamp,
            }
            for metric in metrics
        ]
        self.client.write_points(points)