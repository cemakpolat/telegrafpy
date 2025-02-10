# plugins/inputs/network_input.py
import psutil
from base import Metric, InputPlugin

class NetworkInputPlugin(InputPlugin):
    def gather(self) -> list[Metric]:
        # Collect network I/O metrics
        net_io = psutil.net_io_counters()

        # Create metrics
        metrics = [
            Metric(
                name="network",
                tags={"host": "localhost"},
                fields={
                    "bytes_sent": net_io.bytes_sent,
                    "bytes_recv": net_io.bytes_recv,
                    "packets_sent": net_io.packets_sent,
                    "packets_recv": net_io.packets_recv,
                    "errin": net_io.errin,
                    "errout": net_io.errout,
                    "dropin": net_io.dropin,
                    "dropout": net_io.dropout,
                },
            )
        ]
        return metrics