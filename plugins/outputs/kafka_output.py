# plugins/outputs/kafka_output.py
from kafka import KafkaProducer
import json
from ..metric import Metric

class KafkaOutputPlugin:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def write(self, metrics: list[Metric]):
        for metric in metrics:
            self.producer.send(self.topic, metric.__dict__)