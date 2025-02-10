from telegrafpy.base import Metric


class Filter:
    def __init__(self, namepass=None, namedrop=None, tagpass=None, tagdrop=None):
        self.namepass = namepass or []
        self.namedrop = namedrop or []
        self.tagpass = tagpass or {}
        self.tagdrop = tagdrop or {}

    def filter_metric(self, metric: Metric) -> bool:
        # Apply namepass and namedrop filters
        if self.namepass and metric.name not in self.namepass:
            return False
        if self.namedrop and metric.name in self.namedrop:
            return False

        # Apply tagpass and tagdrop filters
        for key, values in self.tagpass.items():
            if key not in metric.tags or metric.tags[key] not in values:
                return False
        for key, values in self.tagdrop.items():
            if key in metric.tags and metric.tags[key] in values:
                return False

        return True
