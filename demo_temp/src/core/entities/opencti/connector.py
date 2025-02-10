from queue import Queue
from typing import TYPE_CHECKING

from demo_temp.src.utils.singleton import singleton

if TYPE_CHECKING:
    from demo_temp.src.core.entities.opencti.config import Config
    from demo_temp.src.core.entities.opencti.octi_helper import (
        OctiHelper,
    )
    from demo_temp.src.core.entities.producer import Producer
    from demo_temp.src.core.entities.worker import Worker


@singleton
class Connector:

    def __init__(self, config: "Config", helper: "OctiHelper") -> None:
        self._config = config
        self._helper = helper.helper
        self._logger = self._helper.connector_logger
        self._log_debug("Connector initialized TEEEESSSSTTT")
        self._producers = {}
        self._workers = {}
        self._queues = {}

    def _log_debug(self, debug_message: str) -> None:
        # to connector logger
        self._logger.debug(message=debug_message)

    def register_producer(self, name: str, producer_cls: "Producer") -> None:
        self._producers[name] = producer_cls
        self._queues[name] = Queue()

    def register_worker(self, name: str, worker_cls: "Worker") -> None:
        self._workers[name] = worker_cls

    def get_producer(self, name: str) -> "Producer":
        if name in self._producers:
            return self._producers[name](self._queues[name])
        raise ValueError(f"Producer '{name}' not found")

    def start_worker(self, name: str) -> None:
        if name in self._workers and name in self._queues:
            worker = self._workers[name](self._queues[name])
            if not worker.running:
                worker.start()
                worker.join()

    def _process_callback(self) -> None:
        self._log_debug("Connector CALLLLEEEED")
        self._log_debug(f"Producers: {self._producers.keys()}")
        for name in self._producers.keys():
            producer = self.get_producer(name)
            producer.produce()
            self.start_worker(name)

    def start(self) -> None:
        """Schedule periodic execution of _process_callback"""
        self._log_debug("Connector SCHEEEDULED")
        self._helper.schedule_iso(
            message_callback=self._process_callback,
            duration_period=self._config.connector.duration_period,
        )
