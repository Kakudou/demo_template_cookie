from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from demo_temp.src.application.connector import Connector
    from demo_temp.src.core.usecases.opencti.create_connector.create_connector_contract_builder import (
        CreateConnectorContractBuilder,
    )

from demo_temp.src.core.usecases.opencti.create_connector.create_connector_contract import (
    CreateConnectorContract,
)


@dataclass
class CreateConnectorContractBuilder:

    _contract: CreateConnectorContract

    def __init__(self) -> None: ...

    def create(self) -> "CreateConnectorContractBuilder":
        self._contract = CreateConnectorContract()
        return self

    def with_error(self, error: str) -> "CreateConnectorContractBuilder":
        self._contract.error = error
        return self

    def with_connector(
        self, connector: "Connector"
    ) -> "CreateConnectorContractBuilder":
        self._contract.connector = connector
        return self

    def build(self) -> CreateConnectorContract:
        return self._contract
