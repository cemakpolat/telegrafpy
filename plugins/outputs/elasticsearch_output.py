# plugins/outputs/elasticsearch_output.py
from elasticsearch import Elasticsearch
from ..metric import Metric

class ElasticsearchOutputPlugin:
    def __init__(self, hosts: list):
        self.client = Elasticsearch(hosts)

    def write(self, metrics: list[Metric]):
        for metric in metrics:
            self.client.index(index="metrics", body=metric.__dict__)