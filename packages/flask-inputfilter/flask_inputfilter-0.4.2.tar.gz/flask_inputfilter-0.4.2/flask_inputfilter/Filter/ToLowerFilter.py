from __future__ import annotations

from typing import Any, Union

from flask_inputfilter.Filter import BaseFilter


class ToLowerFilter(BaseFilter):
    """
    Filter that converts a string to lowercase.
    """

    def apply(self, value: Any) -> Union[str, Any]:
        if not isinstance(value, str):
            return value

        return value.lower()
