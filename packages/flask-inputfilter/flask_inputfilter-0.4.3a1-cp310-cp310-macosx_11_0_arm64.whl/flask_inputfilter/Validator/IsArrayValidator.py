from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class IsArrayValidator(BaseValidator):
    """
    Validator that checks if a value is an array.
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        if not isinstance(value, list):
            raise ValidationError(
                self.error_message or f"Value '{value}' is not an array."
            )
