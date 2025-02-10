"""Module to test the OpenCTI fail with invalid configuration."""

from os import environ as os_environ
from os import getcwd as os_getcwd
from os import path as os_path
from typing import Any
from unittest.mock import patch

from pytest import raises as pytest_raises
from pytest_bdd import given, parsers, scenario, then, when

from demo_temp.src.application.connector import Connector
from demo_temp.src.utils.errors import ConfigLoaderError

CURRENT_FILE = os_path.dirname(os_path.dirname(os_path.abspath(__file__)))
EXECUTION_DIR = os_getcwd()
GHERKIN_RELATIVE_PATH = f"{EXECUTION_DIR}/gherkin_files/constraints"


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
    f"{GHERKIN_RELATIVE_PATH}/opencti/implemented/connector_fail_invalid_configuration.feature",
    "Fail to instantiate connector due to invalid configuration.",
)
def test_connector_config_load() -> None:
    """Test the OpenCTI fail with invalid configuration."""
    pass


@given(
    parsers.parse(
        "an invalid 'config.yaml' file with invalid or missing value for {opencti_url}, {opencti_token}, {connector_id}, {connector_name}, {connector_scope}, {connector_log_level} , {connector_duration_period}, {connector_type}."
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
        "CONNECTOR_TYPE": connector_type,
        "CONNECTOR_NAME": connector_name,
        "CONNECTOR_SCOPE": connector_scope,
        "CONNECTOR_LOG_LEVEL": connector_log_level,
        "CONNECTOR_DURATION_PERIOD": connector_duration_period,
    }

    mock_env = _mock_env_vars(os_environ, mock_env)
    mock_api, mock_healthcheck, mock_query = _mock_opencti_api_client()

    return {
        "mock_env": mock_env,
        "mock_api": mock_api,
        "mock_healthcheck": mock_healthcheck,
        "mock_query": mock_query,
    }


@when(
    parsers.parse(
        "the try-to-instantiate connector attempts to parse the configuration file."
    )
)
def when_connector_config_load(context: dict[str, Any]) -> None:
    """Configure the OpenCTI connector."""
    with pytest_raises(ConfigLoaderError) as error:
        Connector()

    context["error"] = str(error.value)


@then(
    parsers.parse("an error should be logged indicating configuration issues.")
)
def then_connector_config_load(context: dict[str, Any]) -> None:
    """Check if the error message is as expected."""
    assert (  # noqa: S101
        context["error"] == "Unable to retrieve connector log level in config"
        or context["error"]
        == "Unable to retrieve connector duration period in config"
    )

    _stop_all_mocks(context)
