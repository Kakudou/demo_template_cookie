from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from demo_temp.src.application.connector import Connector


@dataclass
class CreateConnectorContract:
    error: str | None = None
    connector: "Connector" = None
