# plugins/outputs/redis_output.py
import redis
from ..metric import Metric

class RedisOutputPlugin:
    def __init__(self, host: str, port: int, db: int = 0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def write(self, metrics: list[Metric]):
        for metric in metrics:
            self.client.set(metric.name, json.dumps(metric.__dict__))