# plugins/inputs/syslog_input.py
import socket
from ..metric import Metric

class SyslogInputPlugin:
    def __init__(self, host: str = "0.0.0.0", port: int = 514):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    def gather(self) -> list[Metric]:
        data, addr = self.sock.recvfrom(1024)
        metrics = [
            Metric(
                name="syslog",
                tags={"source": addr[0]},
                fields={"message": data.decode("utf-8")},
            )
        ]
        return metrics