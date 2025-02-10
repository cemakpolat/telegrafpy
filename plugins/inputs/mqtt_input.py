import paho.mqtt.client as mqtt
from base import Metric,InputPlugin

class MQTTInputPlugin(InputPlugin):
    def __init__(self, broker: str, port: int, topic: str):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.metrics = []

        # Set up MQTT client
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port)
        self.client.subscribe(self.topic)
        self.client.loop_start()

    def on_message(self, client, userdata, msg):
        metric = Metric(
            name="mqtt",
            tags={"topic": msg.topic},
            fields={"value": msg.payload.decode()},
        )
        self.metrics.append(metric)

    def gather(self) -> list[Metric]:
        metrics = self.metrics
        self.metrics = []
        return metrics