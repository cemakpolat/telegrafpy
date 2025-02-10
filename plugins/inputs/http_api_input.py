# plugins/inputs/http_api_input.py
import requests
from base import Metric, InputPlugin

class HTTPAPIInputPlugin(InputPlugin):
    def __init__(self, url: str, interval: int = 5):
        self.url = url
        self.interval = interval

    def gather(self) -> list[Metric]:
        try:
            # Make an HTTP GET request to the API
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse the response as JSON
            data = response.json()

            # Create metrics from the API response
            metrics = [
                Metric(
                    name="http_api",
                    tags={"url": self.url},
                    fields=data,  # Use the entire JSON response as fields
                )
            ]
            return metrics
        except Exception as e:
            print(f"Error fetching data from HTTP API: {e}")
            return []