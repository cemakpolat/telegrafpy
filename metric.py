

# Example Input Plugin (CPU Metrics)

# MQTT Input Plugin
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
        # Convert MQTT message to a metric
        metric = Metric(
            name="mqtt",
            tags={"topic": msg.topic},
            fields={"value": msg.payload.decode()},
        )
        self.metrics.append(metric)

    def gather(self) -> List[Metric]:
        # Return collected metrics and clear the buffer
        metrics = self.metrics
        self.metrics = []
        return metrics

# Example Processor (Add a Tag)
class AddTagProcessor(Processor):
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def process(self, metrics: List[Metric]) -> List[Metric]:
        for metric in metrics:
            metric.tags[self.key] = self.value
        return metrics

# Python Code Processor
class PythonCodeProcessor(Processor):
    def __init__(self, code: str):
        self.code = code

    def process(self, metrics: List[Metric]) -> List[Metric]:
        def process_metric(metric: Metric) -> Metric:
            locals_dict = {"metric": metric}
            exec(self.code, globals(), locals_dict)
            return locals_dict.get("metric", metric)

        return [process_metric(metric) for metric in metrics]

