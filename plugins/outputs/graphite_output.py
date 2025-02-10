# plugins/outputs/graphite_output.py
import socket
from ..metric import Metric

class GraphiteOutputPlugin:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def write(self, metrics: list[Metric]):
        sock = socket.socket()
        sock.connect((self.host, self.port))
        for metric in metrics:
            message = f"{metric.name} {metric.fields['value']} {metric.timestamp}\n"
            sock.sendall(message.encode("utf-8"))
        sock.close()