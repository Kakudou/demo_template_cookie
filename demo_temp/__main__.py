"""Entry point for the demo_temp package."""

from os import environ as os_environ
from sys import exit
from unittest.mock import patch
from uuid import uuid4

from demo_temp.src.application.connector import Connector
from template_connector.src.core.usecases.fetch_sariel_api import FetchSarielAPI
from template_connector.src.core.usecases.process_sariel_data import ProcessSarielData


def dev_env() -> dict[str, str]:
    """Development environment variables used for testing through mock patching."""
    return {
        "OPENCTI_URL": "http://localhost:8080",
        "OPENCTI_TOKEN": f"{os_environ.get('OCTI_TOKEN')}",
        "CONNECTOR_ID": f"{uuid4()}",
        "CONNECTOR_TYPE": "EXTERNAL_IMPORT",
        "CONNECTOR_NAME": "DemoTemp",
        "CONNECTOR_SCOPE": "all",
        "CONNECTOR_DURATION_PERIOD": "PT1M",
        "CONNECTOR_LOG_LEVEL": "debug",
    }


def connector() -> int:
    """Entry point for the demo_temp package."""
    env_vars = dev_env() if os_environ.get("OCTI_DEV") == "DEV" else os_environ

    dev_patch = patch.dict(os_environ, env_vars)
    dev_patch.start()

    connector = Connector()

    connector.register_producer("sari3l", FetchSarielAPI)
    connector.register_worker("sari3l", ProcessSarielData)

    connector.start()

    dev_patch.stop()
    return 0


if __name__ == "__main__":
    exit(connector())
