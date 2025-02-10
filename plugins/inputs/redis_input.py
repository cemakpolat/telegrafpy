# plugins/inputs/redis_input.py
import redis
from ..metric import Metric

class RedisInputPlugin:
    def __init__(self, host: str, port: int, db: int = 0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def gather(self) -> list[Metric]:
        metrics = []
        keys = self.client.keys("*")
        for key in keys:
            value = self.client.get(key)
            metrics.append(
                Metric(
                    name="redis",
                    tags={"key": key.decode("utf-8")},
                    fields={"value": value.decode("utf-8")},
                )
            )
        return metrics