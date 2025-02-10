# plugins/inputs/grpc_input.py
import grpc
from ..metric import Metric

class GRPCInputPlugin:
    def __init__(self, server_address: str):
        self.server_address = server_address
        self.channel = grpc.insecure_channel(self.server_address)

    def gather(self) -> list[Metric]:
        # Example: Call a gRPC service to get metrics
        # Replace with your actual gRPC service and method
        response = self.stub.GetMetrics(request_pb2.MetricsRequest())
        metrics = [
            Metric(
                name="grpc",
                tags={"service": "example"},
                fields={"value": response.value},
            )
        ]
        return metrics