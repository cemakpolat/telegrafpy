# plugins/inputs/docker_input.py
import docker
from ..metric import Metric

class DockerInputPlugin:
    def __init__(self):
        self.client = docker.from_env()

    def gather(self) -> list[Metric]:
        metrics = []
        for container in self.client.containers.list():
            stats = container.stats(stream=False)
            metrics.append(
                Metric(
                    name="docker",
                    tags={"container_id": container.id},
                    fields={
                        "cpu_usage": stats["cpu_stats"]["cpu_usage"]["total_usage"],
                        "memory_usage": stats["memory_stats"]["usage"],
                    },
                )
            )
        return metrics