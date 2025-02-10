# plugins/inputs/kafka_input.py
from kafka import KafkaConsumer
import json
from ..metric import Metric

class KafkaInputPlugin:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )

    def gather(self) -> list[Metric]:
        metrics = []
        for message in self.consumer:
            data = message.value
            metrics.append(
                Metric(
                    name="kafka",
                    tags={"topic": self.topic},
                    fields=data,
                )
            )
        return metrics