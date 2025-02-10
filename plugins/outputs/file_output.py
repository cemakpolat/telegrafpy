# plugins/outputs/file_output.py
import json
from base import Metric, OutputPlugin

class FileOutputPlugin(OutputPlugin):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def write(self, metrics: list[Metric]):
        try:
            # Convert metrics to JSON
            metrics_json = [metric.__dict__ for metric in metrics]

            # Write metrics to the file
            with open(self.file_path, "a") as f:
                for metric in metrics_json:
                    f.write(json.dumps(metric) + "\n")
        except Exception as e:
            print(f"Error writing metrics to file: {e}")