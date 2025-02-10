# import argparse
import queue

import toml
import time
from plugins.inputs import *
from plugins.processors.add_tag import AddTagProcessor
from plugins.processors.python_code import PythonCodeProcessor
from plugins.processors.external_executable import ExternalExecutableProcessor
from plugins.outputs import *
from concurrent.futures import ThreadPoolExecutor

class PluginManager:
    def __init__(self, inputs, processors, outputs,global_interval: int = 5, max_workers: int = 5):
        self.inputs = inputs
        self.processors = processors
        self.outputs = outputs
        self.global_interval = global_interval
        self.metric_queue = queue.Queue()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)  # Thread pool


    def run(self):
        # Submit input plugins to the thread pool
        for input_plugin in self.inputs:
            self.executor.submit(self.run_input_plugin, input_plugin)

            # Main processing loop
            while True:
                # Collect metrics from the queue
                metrics = []
                while not self.metric_queue.empty():
                    metrics.append(self.metric_queue.get())

                # Process metrics
                for processor in self.processors:
                    metrics = processor.process(metrics)

                # Write metrics to output plugins
                for output_plugin in self.outputs:
                    output_plugin.write(metrics)

                time.sleep(self.global_interval)

    def run_input_plugin(self, input_plugin):
        interval = getattr(input_plugin, "interval", self.global_interval)
        while True:
            metrics = input_plugin.gather()
            for metric in metrics:
                self.metric_queue.put(metric)  # Add metrics to the queue
            time.sleep(interval)


def load_config(file_path: str) -> dict:
    with open(file_path, "r") as f:
        return toml.load(f)


def initialize_plugins(config: dict):
    inputs = []
    processors = []
    outputs = []

    if "inputs" in config:
        if "cpu" in config["inputs"]:
            cpu_config = config["inputs"]["cpu"]
            # inputs.append(CPUInputPlugin(
            #     interval=cpu_config.get("interval", config["plugin_manager"]["global_interval"]),
            # ))
            cpu_config = config["inputs"]["cpu"]
            inputs.append(CPUInputPlugin(
                interval=cpu_config.get("interval", config["plugin_manager"]["global_interval"]),
                namepass=cpu_config.get("namepass"),
                namedrop=cpu_config.get("namedrop"),
                tagpass=cpu_config.get("tagpass"),
                tagdrop=cpu_config.get("tagdrop"),
            ))
    if "inputs" in config:
        if "cpu" in config["inputs"]:
            cpu_config = config["inputs"]["cpu"]
            inputs.append(CPUInputPlugin(
                interval=cpu_config.get("interval", config["plugin_manager"]["global_interval"]),
            ))
        if "ram" in config["inputs"]:
            inputs.append(RAMInputPlugin())  # Add RAM input plugin
        if "network" in config["inputs"]:
            inputs.append(NetworkInputPlugin())  # Add Network input plugin
        if "mqtt" in config["inputs"]:
            mqtt_config = config["inputs"]["mqtt"]
            inputs.append(MQTTInputPlugin(
                broker=mqtt_config["broker"],
                port=mqtt_config["port"],
                topic=mqtt_config["topic"],
            ))
        if "http_api" in config["inputs"]:
            http_api_config = config["inputs"]["http_api"]
            inputs.append(HTTPAPIInputPlugin(
                url=http_api_config["url"],
                interval=http_api_config.get("interval", 5),
            ))
        if "websocket" in config["inputs"]:
            websocket_config = config["inputs"]["websocket"]
            inputs.append(WebSocketInputPlugin(
                uri=websocket_config["uri"],
            ))

    if "processors" in config:
        if "add_tag" in config["processors"]:
            add_tag_config = config["processors"]["add_tag"]
            processors.append(AddTagProcessor(
                key=add_tag_config["key"],
                value=add_tag_config["value"],
                namepass=add_tag_config.get("namepass"),
                namedrop=add_tag_config.get("namedrop"),
                tagpass=add_tag_config.get("tagpass"),
                tagdrop=add_tag_config.get("tagdrop"),
            ))
        if "python_code" in config["processors"]:
            python_code_config = config["processors"]["python_code"]
            processors.append(PythonCodeProcessor(
                code=python_code_config["code"],
            ))
        if "external_executable" in config["processors"]:
            external_executable_config = config["processors"]["external_executable"]
            processors.append(ExternalExecutableProcessor(
                command=external_executable_config["command"],
            ))

    if "outputs" in config:
        if "mqtt" in config["outputs"]:
            mqtt_config = config["outputs"]["mqtt"]
            outputs.append(MQTTOutputPlugin(
                broker=mqtt_config["broker"],
                port=mqtt_config["port"],
                topic=mqtt_config["topic"],
            ))
        if "console" in config["outputs"]:
            console_config = config["outputs"]["console"]
            outputs.append(ConsoleOutputPlugin(
                namepass=console_config.get("namepass"),
                namedrop=console_config.get("namedrop"),
                tagpass=console_config.get("tagpass"),
                tagdrop=console_config.get("tagdrop"),
            ))
        if "file" in config["outputs"]:
            file_config = config["outputs"]["file"]
            outputs.append(FileOutputPlugin(
                file_path=file_config["path"],
            ))
        if "http" in config["outputs"]:
            http_config = config["outputs"]["http"]
            outputs.append(HTTPOutputPlugin(
                url=http_config["url"],
            ))

        # Get the global interval and max_workers from the configuration
    global_interval = config["plugin_manager"]["global_interval"]
    max_workers = config["plugin_manager"].get("max_workers", 5)

    return inputs, processors, outputs, global_interval, max_workers


def main():
    # parser = argparse.ArgumentParser(description="Telegraf-like tool for collecting and processing metrics.")
    # parser.add_argument("--config", required=True, help="Path to the configuration file.")
    # args = parser.parse_args()

    # config = load_config(args.config)
    config = load_config("./config/config.toml")

    inputs, processors, outputs, global_interval,max_worker = initialize_plugins(config)
    manager = PluginManager(inputs, processors, outputs, global_interval, max_worker)
    manager.run()


if __name__ == "__main__":
    main()
