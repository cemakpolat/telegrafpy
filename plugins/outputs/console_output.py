from base import Metric,OutputPlugin

from telegrafpy.filter import Filter


class ConsoleOutputPlugin:
    def __init__(self, namepass=None, namedrop=None, tagpass=None, tagdrop=None):
        self.filter = Filter(namepass, namedrop, tagpass, tagdrop)

    def write(self, metrics: list[Metric]):
        for metric in metrics:
            if self.filter.filter_metric(metric):
                print(metric)