from base import Metric,Processor

from telegrafpy.filter import Filter


class AddTagProcessor:
    def __init__(self, key: str, value: str, namepass=None, namedrop=None, tagpass=None, tagdrop=None):
        self.key = key
        self.value = value
        self.filter = Filter(namepass, namedrop, tagpass, tagdrop)

    def process(self, metrics: list[Metric]) -> list[Metric]:
        processed_metrics = []
        for metric in metrics:
            if self.filter.filter_metric(metric):
                metric.tags[self.key] = self.value
            processed_metrics.append(metric)
        return processed_metrics