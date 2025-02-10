from abc import ABC, abstractmethod
from typing import Dict, Any, List
import time


class Metric:
    def __init__(self, name: str, tags: Dict[str, str], fields: Dict[str, Any], timestamp: int = None):
        self.name = name
        self.tags = tags
        self.fields = fields
        self.timestamp = timestamp or int(time.time())

    def __repr__(self):
        return f"Metric(name={self.name}, tags={self.tags}, fields={self.fields}, timestamp={self.timestamp})"


# InputPlugin defines the interface for input plugins
class InputPlugin(ABC):
    @abstractmethod
    def gather(self) -> List[Metric]:
        pass


# Processor defines the interface for data processors
class Processor(ABC):
    @abstractmethod
    def process(self, metrics: List[Metric]) -> List[Metric]:
        pass


# OutputPlugin defines the interface for output plugins
class OutputPlugin(ABC):
    @abstractmethod
    def write(self, metrics: List[Metric]):
        pass
