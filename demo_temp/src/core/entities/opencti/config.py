from dotenv import load_dotenv

from demo_temp.src.core.entities.opencti.connector_config import (
    ConnectorConfig,
)
from demo_temp.src.core.entities.opencti.opencti_config import (
    OpenCTIConfig,
)
from demo_temp.src.core.entities.opencti.demo_temp_config import (
    DemoTempConfig,
)


class Config:

    def __init__(self):
        load_dotenv()
        self.opencti = OpenCTIConfig()
        self.connector = ConnectorConfig()
        self.demo_temp = DemoTempConfig()

        self.to_dict()

    def to_dict(self) -> dict:
        return {
            "opencti": OpenCTIConfig().to_dict(),
            "connector": ConnectorConfig().to_dict(),
            "demo_temp": DemoTempConfig().to_dict(),
        }
