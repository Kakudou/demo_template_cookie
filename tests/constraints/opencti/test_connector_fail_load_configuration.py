"""Module to test the OpenCTI fail with a missing configuration file."""

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
    f"{GHERKIN_RELATIVE_PATH}/opencti/implemented/connector_fail_load_configuration.feature",
    "Fail to load configuration due to missing file.",
)
def test_connector_config_load() -> None:
    """Test the OpenCTI fail with a missing configuration file."""
    pass


@given(
    parsers.parse("the 'config.yaml' file does not exist."),
    target_fixture="context",
)
def given_connector_config_load() -> dict[str, Any]:
    """Mock the environment variables."""
    mock_env = {}
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
    """Check if the configuration file is loaded successfully."""
    with pytest_raises(ConfigLoaderError) as error:
        Connector()

    context["error"] = str(error.value)


@then(
    parsers.parse(
        "an error should be logged indicating a failure to load the configuration file."
    )
)
def then_connector_config_load(context: dict[str, Any]) -> None:
    """Check if the error message is as expected."""
    assert (  # noqa: S101
        context["error"] == "Unable to retrieve OpenCTI URL in config"
        or context["error"]
        == "Unable to retrieve connector duration period in config"
    )

    _stop_all_mocks(context)
