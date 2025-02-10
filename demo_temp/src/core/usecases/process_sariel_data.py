from demo_temp.src.core.entities.opencti.connector import Connector
from demo_temp.src.core.entities.worker import Worker


class ProcessSarielData(Worker):

    def process(self, data: dict):
        Connector()._logger.debug("TODO, need to implement correct worker processing, but you got the point")

