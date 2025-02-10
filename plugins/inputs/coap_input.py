# plugins/inputs/coap_input.py
import asyncio, json, time
from aiocoap import Context, Message, GET
from base import Metric, InputPlugin

class CoAPInputPlugin(InputPlugin):
    def __init__(self, uri: str, request_interval: int = 5):
        self.uri = uri
        self.request_interval = request_interval
        self.last_request_time = 0

    async def gather(self) -> list[Metric]:
        current_time = time.time()
        if current_time - self.last_request_time < self.request_interval:
            return []  # Skip if the request interval hasn't passed

        self.last_request_time = current_time

        try:
            protocol = await Context.create_client_context()
            request = Message(code=GET, uri=self.uri)
            response = await protocol.request(request).response
            data = json.loads(response.payload.decode("utf-8"))
            return [
                Metric(
                    name="coap",
                    tags={"uri": self.uri},
                    fields=data,
                )
            ]
        except Exception as e:
            print(f"Error fetching data from CoAP endpoint: {e}")
            return []