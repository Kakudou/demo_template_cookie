from abc import ABC, abstractmethod
from queue import Queue


class Producer(ABC):

    def __init__(self, queue: Queue):
        self.queue = queue

    @abstractmethod
    def produce(self):
        pass
