from typing import Any

from pycti import (
    get_config_variable,  # type: ignore[import-untyped]; pycti does not provide stubs
)


class PyCTIUtils:

    @classmethod
    def get_config_variable_env(
        cls, env_var: str, required: bool = False
    ) -> Any:
        value = get_config_variable(env_var=env_var, yaml_path=["", ""])
        if value is None and required:
            raise ValueError(
                f"Environment variable {env_var} is required but not set."
            )
        # see https://github.com/OpenCTI-Platform/client-python/issues/817
        return value
