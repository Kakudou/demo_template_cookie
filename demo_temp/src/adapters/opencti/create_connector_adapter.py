from contextlib import suppress
from dataclasses import dataclass

from pycti import (  # type: ignore[import-untyped] # pycti does not provide stubs
    OpenCTIConnectorHelper,
)

from demo_temp.src.core.entities.opencti.octi_helper import (
    OctiHelper as AbstractOctiHelper,
)
from demo_temp.src.core.usecases.opencti.create_connector.create_connector import CreateConnector
from demo_temp.src.core.usecases.opencti.create_connector.create_connector_port_builder import (
    CreateConnectorPortBuilder,
)


class CreateConnectorAdapter:

    @staticmethod
    def execute():

        @dataclass
        class OctiHelper(AbstractOctiHelper):
            helper: OpenCTIConnectorHelper

            def __init__(self):
                with suppress(ValueError):
                    self.helper = OpenCTIConnectorHelper(config={})

            def config(self, config: dict) -> None:
                self.helper.config = config

        adapter_builder = CreateConnectorPortBuilder()
        adapter = (
            adapter_builder.create().with_octi_helper(OctiHelper()).build()
        )

        contract = CreateConnector().execute(adapter)

        return contract
