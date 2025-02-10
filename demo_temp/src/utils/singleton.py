"""The module mananges the singleton."""

from typing import Any, Dict


def singleton(class_: Any) -> Any:
    """Create or return a singleton instance.

    Functions:
    ----------
    getinstance:
        return the singleton
    """
    __instances: Dict[Any, Any] = {}

    def getinstance(*args: Any, **kwargs: Any) -> Any:
        """Create or return the singleton instance."""
        if class_ not in __instances:
            __instances[class_] = class_(*args, **kwargs)
        return __instances[class_]

    return getinstance
