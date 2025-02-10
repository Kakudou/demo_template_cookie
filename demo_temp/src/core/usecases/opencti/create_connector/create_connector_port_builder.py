from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from demo_temp.src.core.entities.opencti.octi_helper import (
        OctiHelper,
    )

from demo_temp.src.core.usecases.opencti.create_connector.create_connector_port import (
    CreateConnectorPort,
)


@dataclass
class CreateConnectorPortBuilder:
    _port: CreateConnectorPort

    def __init__(self): ...

    def create(self) -> "CreateConnectorPortBuilder":
        self._port = CreateConnectorPort()
        return self

    def with_octi_helper(
        self, octi_helper: "OctiHelper"
    ) -> "CreateConnectorPortBuilder":
        self._port.octi_helper = octi_helper
        return self

    def build(self) -> CreateConnectorPort:
        return self._port
