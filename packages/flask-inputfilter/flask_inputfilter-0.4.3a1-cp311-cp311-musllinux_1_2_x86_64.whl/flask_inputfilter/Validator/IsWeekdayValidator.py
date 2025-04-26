from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class IsWeekdayValidator(BaseValidator):
    """
    Validator that checks if a date is on a weekday (Monday to Friday).
    Supports datetime and ISO 8601 formatted strings.
    """

    __slots__ = ("error_message",)

    def __init__(self, error_message: Optional[str] = None) -> None:
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        value_datetime = self.__parse_date(value)

        if value_datetime.weekday() in (5, 6):
            raise ValidationError(
                self.error_message or f"Date '{value}' is not a weekday."
            )

    @staticmethod
    def __parse_date(value: Any) -> datetime:
        if isinstance(value, datetime):
            return value

        elif isinstance(value, date):
            return datetime.combine(value, datetime.min.time())

        elif isinstance(value, str):
            try:
                return datetime.fromisoformat(value)

            except ValueError:
                raise ValidationError(f"Invalid ISO 8601 format '{value}'.")

        raise ValidationError(
            f"Unsupported type for weekday validation '{type(value)}'."
        )
