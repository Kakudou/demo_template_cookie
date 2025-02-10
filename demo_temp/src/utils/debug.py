"""Tools for debugging."""

from typing import Any


class Debug:
    """Various debugging tools.

    Functions:
    ----------
    dump: staticmethod
        dump an object

    """

    @staticmethod
    def dump(object: Any, attrs: Any = None) -> None:
        """Dump an object.

        Parameters
        -----------
        object: Any
            object to dump
        attrs: Any
            attributes to dump

        """
        print(  # noqa: T201 # printing to console is the goal here
            "\n#### Start Dump ####"
        )
        if attrs is None:
            ptr = dir(object)
        else:
            ptr = attrs
        for attr in ptr:
            print(  # noqa: T201 # printing to console is the goal here
                "object.%s = %r" % (attr, getattr(object, attr))
            )
        print(  # noqa: T201 # printing to console is the goal here
            "#### Ended Dump ####\n"
        )
