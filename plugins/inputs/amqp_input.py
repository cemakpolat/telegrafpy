# plugins/inputs/amqp_input.py
import pika
from ..metric import Metric

class AMQPInputPlugin:
    def __init__(self, queue: str, host: str = "localhost", port: int = 5672):
        self.queue = queue
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=port)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def gather(self) -> list[Metric]:
        metrics = []
        method_frame, header_frame, body = self.channel.basic_get(queue=self.queue)
        if method_frame:
            metrics.append(
                Metric(
                    name="amqp",
                    tags={"queue": self.queue},
                    fields={"message": body.decode("utf-8")},
                )
            )
            self.channel.basic_ack(method_frame.delivery_tag)
        return metrics