import json
import sys

# Read the input metric from stdin
input_metric = sys.stdin.read()
# Parse the input metric
metric_data = json.loads(input_metric)

# Modify the metric
metric_data["fields"]["processed_by_external"] = True

# Output the modified metric as JSON
print(json.dumps(metric_data))