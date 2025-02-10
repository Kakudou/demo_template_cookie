from abc import ABC, abstractmethod
from typing import Any


class OctiHelper(ABC):

    helper: Any

    @abstractmethod
    def config(self, config: dict) -> None: ...
