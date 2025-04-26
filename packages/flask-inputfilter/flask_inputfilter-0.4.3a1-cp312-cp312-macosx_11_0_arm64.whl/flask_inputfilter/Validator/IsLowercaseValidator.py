from __future__ import annotations

from typing import Any, Optional

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class IsLowercaseValidator(BaseValidator):
    """
    Validator that checks if a value is entirely lowercase.
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = (
            error_message or "Value is not entirely lowercase."
        )

    def validate(self, value: Any) -> None:
        if not isinstance(value, str):
            raise ValidationError("Value must be a string.")
        if not value.islower():
            raise ValidationError(self.error_message)
