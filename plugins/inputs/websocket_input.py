# plugins/inputs/websocket_input.py
import asyncio
import websockets
import json
from base import Metric, InputPlugin

class WebSocketInputPlugin(InputPlugin):
    def __init__(self, uri: str):
        self.uri = uri

    async def gather(self) -> list[Metric]:
        try:
            async with websockets.connect(self.uri) as websocket:
                # Receive data from the WebSocket
                data = await websocket.recv()

                # Parse the data as JSON
                data = json.loads(data)

                # Create metrics from the WebSocket data
                metrics = [
                    Metric(
                        name="websocket",
                        tags={"uri": self.uri},
                        fields=data,  # Use the entire JSON data as fields
                    )
                ]
                return metrics
        except Exception as e:
            print(f"Error receiving data from WebSocket: {e}")
            return []