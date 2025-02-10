from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from demo_temp.src.core.entities.opencti.octi_helper import (
        OctiHelper,
    )


@dataclass
class CreateConnectorPort:
    octi_helper: "OctiHelper"

    def __init__(self): ...
