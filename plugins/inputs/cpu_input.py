from base import Metric, Processor
from base import InputPlugin
import psutil
import logging

from telegrafpy.filter import Filter

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# class CPUInputPlugin(InputPlugin):
#     def __init__(self, interval: int = 5):
#         self.interval = interval
#
#     def gather(self) -> list[Metric]:
#         # Collect CPU usage metrics
#         cpu_percent = psutil.cpu_percent(interval=1)
#         cpu_count = psutil.cpu_count(logical=True)
#         cpu_times = psutil.cpu_times()
#
#         # Create metrics
#         metrics = [
#             Metric(
#                 name="cpu",
#                 tags={"host": "localhost"},
#                 fields={
#                     "usage_percent": cpu_percent,
#                     "cpu_count": cpu_count,
#                     "user_time": cpu_times.user,
#                     "system_time": cpu_times.system,
#                     "idle_time": cpu_times.idle,
#                 },
#             )
#         ]
#
#         logging.info(f"Collected CPU metrics: {metrics}")
#         return metrics
#

class CPUInputPlugin:
    def __init__(self, interval: int = 5, namepass=None, namedrop=None, tagpass=None, tagdrop=None):
        self.interval = interval
        self.filter = Filter(namepass, namedrop, tagpass, tagdrop)

    def gather(self) -> list[Metric]:
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count(logical=True)
        cpu_times = psutil.cpu_times()

        metric = Metric(
            name="cpu",
            tags={"host": "localhost"},
            fields={
                "usage_percent": cpu_percent,
                "cpu_count": cpu_count,
                "user_time": cpu_times.user,
                "system_time": cpu_times.system,
                "idle_time": cpu_times.idle,
            },
        )

        # Apply the filter
        if self.filter.filter_metric(metric):
            print("metric", metric)
            return [metric]
        return []