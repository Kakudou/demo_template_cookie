from demo_temp.src.utils.errors import _make_error_handler
from demo_temp.src.utils.pycti_utils import PyCTIUtils


class OpenCTIConfig:
    @property
    def _url(self) -> str:
        return PyCTIUtils.get_config_variable_env(env_var="OPENCTI_URL", required=True)  # type: ignore[no-any-return]

    @property
    @_make_error_handler("Unable to retrieve OpenCTI URL in config")
    def url(self) -> str:
        """URL for OpenCTI API."""
        return self._url

    @property
    def _token(self) -> str:
        return PyCTIUtils.get_config_variable_env(env_var="OPENCTI_TOKEN", required=True)  # type: ignore[no-any-return]

    @property
    @_make_error_handler("Unable to retrieve OpenCTI Token in config")
    def token(self) -> str:
        return self._token

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "token": self.token,
        }
