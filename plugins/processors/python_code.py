from base import Metric,Processor

class PythonCodeProcessor(Processor):
    def __init__(self, code: str):
        self.code = code

    def process(self, metrics: list[Metric]) -> list[Metric]:
        def process_metric(metric: Metric) -> Metric:
            locals_dict = {"metric": metric}
            exec(self.code, globals(), locals_dict)
            return locals_dict.get("metric", metric)

        return [process_metric(metric) for metric in metrics]