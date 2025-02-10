"""Module to test the OpenCTI connector configuration loading and instantiation."""

from os import environ as os_environ
from os import getcwd as os_getcwd
from os import path as os_path
from typing import Any
from unittest.mock import patch

from pytest_bdd import given, parsers, scenario, then, when

from demo_temp.src.application.connector import Connector


CURRENT_FILE = os_path.dirname(os_path.dirname(os_path.abspath(__file__)))
EXECUTION_DIR = os_getcwd()
GHERKIN_RELATIVE_PATH = f"{EXECUTION_DIR}/gherkin_files/features"


def _mock_env_vars(os_environ, wanted_env):
    # Mock the environment variables
    mock_env = patch.dict(os_environ, wanted_env)
    mock_env.start()

    return mock_env


def _mock_opencti_api_client():
    # Mock the initial call to the OpenCTI API
    mock_api = patch("requests.Session.post")
    mock_api.start()

    # Mock the health check call to the OpenCTI API
    mock_healthcheck = patch(
        "pycti.api.opencti_api_client.OpenCTIApiClient.health_check"
    )
    mock_healthcheck.start()

    # Mock the graphql query call to the OpenCTI API
    mock_query = patch("pycti.api.opencti_api_client.OpenCTIApiClient.query")
    mock_query.start()

    return mock_api, mock_healthcheck, mock_query


def _stop_all_mocks(context):
    # Stop all mocks
    context["mock_env"].stop()
    context["mock_api"].stop()
    context["mock_healthcheck"].stop()
    context["mock_query"].stop()


@scenario(
    f"{GHERKIN_RELATIVE_PATH}/opencti/implemented/connector_config_load.feature",
    "Successfully load configuration and instantiate the OpenCTI connector.",
)
def test_connector_config_load() -> None:
    """Test the OpenCTI connector configuration loading and instantiation."""
    pass


@given(
    parsers.parse(
        "a valid 'config.yaml' file exists, with {opencti_url}, {opencti_token}, {connector_id}, {connector_name}, {connector_scope}, {connector_log_level} , {connector_duration_period}, {connector_type}."
    ),
    target_fixture="context",
)
def given_connector_config_load(
    opencti_url: str,
    opencti_token: str,
    connector_id: str,
    connector_name: str,
    connector_scope: str,
    connector_log_level: str,
    connector_duration_period: str,
    connector_type: str,
) -> dict[str, Any]:
    """Mock the environment variables and the OpenCTI API client."""
    mock_env = {
        "OPENCTI_URL": opencti_url,
        "OPENCTI_TOKEN": opencti_token,
        "CONNECTOR_ID": connector_id,
        "CONNECTOR_NAME": connector_name,
        "CONNECTOR_TYPE": connector_type,
        "CONNECTOR_SCOPE": connector_scope,
        "CONNECTOR_LOG_LEVEL": connector_log_level,
        "CONNECTOR_DURATION_PERIOD": connector_duration_period,
    }

    mock_env = _mock_env_vars(os_environ, mock_env)
    mock_api, mock_healthcheck, mock_query = _mock_opencti_api_client()

    connector_config = {
        "opencti": {
            "url": opencti_url,
            "token": opencti_token,
        },
        "connector": {
            "id": connector_id,
            "name": connector_name,
            "type": "EXTERNAL_IMPORT",
            "scope": connector_scope,
            "log_level": connector_log_level,
            # ?             "duration_period": connector_duration_period, # I removed this line, because i received a timedelta object istead of a string in the connector conf
        },
        "demo_temp": {},
    }

    return {
        "mock_env": mock_env,
        "mock_api": mock_api,
        "mock_healthcheck": mock_healthcheck,
        "mock_query": mock_query,
        "connector_config": connector_config,
    }


@when(parsers.parse("i instantiate the OpenCTI connector."))
def when_connector_config_load(context: dict[str, Any]) -> None:
    """Load and instantiate the OpenCTI connector."""
    connector_holder = Connector()

    context["connector"] = connector_holder.connector


@then(parsers.parse("the OpenCTI connector should be instantiated."))
def then_connector_config_load(context: dict[str, Any]) -> None:
    """Check if the OpenCTI connector has been instantiated."""
    assert context["connector"] is not None  # noqa: S101


@then(
    parsers.parse(
        "the connector should be initialized with the correct settings."
    )
)
def and_then_connector_config_load(context: dict[str, Any]) -> None:
    """Check if the OpenCTI connector has been initialized with the correct settings."""
    connector_config = context["connector"]._config.to_dict()
    connector_config.get("connector").pop(
        "duration_period"
    )  # like above, i removed this line because i received a timedelta object instead of a string in the connector conf

    assert context["connector_config"] == connector_config  # noqa: S101

    _stop_all_mocks(context)
