import os
import subprocess
import json
from base import Metric, Processor

class ExternalExecutableProcessor(Processor):
    def __init__(self, command: str):
        self.command = command

    def process(self, metrics: list[Metric]) -> list[Metric]:
        processed_metrics = []
        for metric in metrics:
            # Serialize the Metric object to JSON
            metric_json = json.dumps(metric.__dict__)

            # Resolve the script path relative to the main executable
            script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../", self.command.split()[-1]))

            # Run the external script
            result = subprocess.run(
                ["python3", script_path],  # Use the resolved script path
                input=metric_json.encode(),  # Pass the JSON-encoded metric
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            if result.returncode == 0:
                output = result.stdout.decode().strip()
                if output:
                    try:
                        # Parse the output as a Metric object
                        metric_data = json.loads(output)
                        processed_metrics.append(Metric(**metric_data))
                    except json.JSONDecodeError:
                        print(f"Error decoding executable output: {output}")
            else:
                print(f"Executable failed with error: {result.stderr.decode()}")

        return processed_metrics