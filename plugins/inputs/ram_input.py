# plugins/inputs/ram_input.py
import psutil
from base import Metric, InputPlugin

class RAMInputPlugin(InputPlugin):
    def gather(self) -> list[Metric]:
        # Collect RAM usage metrics
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        # Create metrics
        metrics = [
            Metric(
                name="ram",
                tags={"host": "localhost"},
                fields={
                    "total": mem.total,
                    "available": mem.available,
                    "used": mem.used,
                    "free": mem.free,
                    "percent": mem.percent,
                    "swap_total": swap.total,
                    "swap_used": swap.used,
                    "swap_free": swap.free,
                    "swap_percent": swap.percent,
                },
            )
        ]
        return metrics