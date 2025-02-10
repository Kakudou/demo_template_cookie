from abc import ABC, abstractmethod
from queue import Queue
from threading import Thread
from typing import Any


class Worker(Thread, ABC):

    def __init__(self, queue: Queue):
        super().__init__(daemon=True)
        self.queue = queue
        self.running = False

    @abstractmethod
    def process(self, data: Any):
        pass

    def run(self):
        self.running = True
        while not self.queue.empty():
            data = self.queue.get()
            self.process(data)
            self.queue.task_done()
        self.running = False

