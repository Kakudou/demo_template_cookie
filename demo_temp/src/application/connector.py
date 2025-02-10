from demo_temp.src.adapters.opencti.create_connector_adapter import (
    CreateConnectorAdapter,
)
from demo_temp.src.utils.singleton import singleton


@singleton
class Connector:

    def __init__(self):
        contract = CreateConnectorAdapter().execute()

        if contract.error is not None:
            exit(1)

        self.connector = contract.connector

    def start(self):
        self.connector.start()

    def register_producer(self, name: str, producer):
        self.connector._logger.info(f"Registering {name} Producer")
        self.connector.register_producer(name, producer)

    def register_worker(self, name: str, worker):
        self.connector._logger.info(f"Registering {name} Worker")
        self.connector.register_worker(name, worker)
