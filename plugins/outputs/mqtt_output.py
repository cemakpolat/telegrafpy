import paho.mqtt.client as mqtt
from base import Metric, OutputPlugin

class MQTTOutputPlugin(OutputPlugin):
    def __init__(self, broker: str, port: int, topic: str):
        self.broker = broker
        self.port = port
        self.topic = topic

        # Set up MQTT client
        self.client = mqtt.Client()
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def write(self, metrics: list[Metric]):
        for metric in metrics:
            message = str(metric.fields)
            self.client.publish(self.topic, message)