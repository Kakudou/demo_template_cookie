from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from demo_temp.src.core.usecases.opencti.create_connector.create_connector_contract import (
        CreateConnectorContract,
    )
    from demo_temp.src.core.usecases.opencti.create_connector.create_connector_port import (
        CreateConnectorPort,
    )

from demo_temp.src.core.entities.opencti.config import Config
from demo_temp.src.core.entities.opencti.connector import Connector
from demo_temp.src.core.entities.opencti.octi_helper import OctiHelper
from demo_temp.src.core.usecases.opencti.create_connector.create_connector_contract_builder import (
    CreateConnectorContractBuilder,
)


@dataclass
class CreateConnector:

    _contract: "CreateConnectorContract"

    def __init__(self) -> None:
        self.contract_builder = CreateConnectorContractBuilder()

    def execute(
        self, input_port: "CreateConnectorPort"
    ) -> "CreateConnectorContract":

        executed = False
        error = None
        connector = None

        connector_config = Config()

        octi_helper: OctiHelper = input_port.octi_helper
        octi_helper.config(connector_config.to_dict())

        try:
            connector = Connector(connector_config, octi_helper)
            executed = True
        except Exception as e:
            error = str(e)

        if executed:
            self._contract = (
                self.contract_builder.create()
                .with_connector(connector)
                .build()
            )
        elif not executed and connector is None:
            if error is None:
                error = "An error occurred while creating the connector."
                self._contract = (
                    self.contract_builder.create().with_error(error).build()
                )

        return self._contract
