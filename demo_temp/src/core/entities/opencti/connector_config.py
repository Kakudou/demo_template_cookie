import datetime
from typing import Literal

from pydantic import TypeAdapter

from demo_temp.src.utils.errors import _make_error_handler
from demo_temp.src.utils.pycti_utils import PyCTIUtils


class ConnectorConfig:
    @property
    def _id(self) -> str:
        return PyCTIUtils.get_config_variable_env(  # type: ignore[no-any-return]
            env_var="CONNECTOR_ID",
            required=True,
        )

    @property
    @_make_error_handler("Unable to retrieve connector ID in config")
    def id(self) -> str:
        """Connector ID."""
        return self._id

    @property
    def _name(self) -> str:
        return PyCTIUtils.get_config_variable_env(  # type: ignore[no-any-return]
            env_var="CONNECTOR_NAME",
            required=True,
        )

    @property
    @_make_error_handler("Unable to retrieve connector name in config")
    def name(self) -> str:
        """Connector name."""
        return self._name

    @property
    def _type(self) -> str:
        return PyCTIUtils.get_config_variable_env(  # type: ignore[no-any-return]
            env_var="CONNECTOR_TYPE",
            required=True,
        )

    @property
    @_make_error_handler("Unable to retrieve connector type in config")
    def type(self) -> str:
        """Connector type."""
        return self._type

    @property
    def _scope(self) -> str:
        return PyCTIUtils.get_config_variable_env(  # type: ignore[no-any-return]
            env_var="CONNECTOR_SCOPE",
            required=True,
        )

    @property
    @_make_error_handler("Unable to retrieve connector scope in config")
    def scope(self) -> str:
        """Connector scope."""
        return self._scope

    @property
    def _log_level(self) -> Literal["debug", "info", "warn", "error"]:
        return PyCTIUtils.get_config_variable_env(  # type: ignore[no-any-return]
            env_var="CONNECTOR_LOG_LEVEL", required=True
        )

    @property
    @_make_error_handler("Unable to retrieve connector log level in config")
    def log_level(self) -> Literal["debug", "info", "warn", "error"]:
        """Connector log level."""
        if self._log_level not in ["debug", "info", "warn", "error"]:
            raise ValueError(
                f"Invalid log level: {self._log_level}. Must be one of 'debug', 'info', 'warn', 'error'"
            )
        return self._log_level

    @property
    def _duration_period(self) -> datetime.timedelta:
        duration_period_str: str = PyCTIUtils.get_config_variable_env(
            env_var="CONNECTOR_DURATION_PERIOD",
            required=True,
        )
        return TypeAdapter(datetime.timedelta).validate_strings(
            duration_period_str
        )

    @property
    @_make_error_handler(
        "Unable to retrieve connector duration period in config"
    )
    def duration_period(self) -> "datetime.timedelta":
        """Connector scheduler settings."""
        return self._duration_period

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "scope": self.scope,
            "log_level": self.log_level,
            "duration_period": self.duration_period,
        }
