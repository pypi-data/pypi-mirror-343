from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional, Union

from flask_inputfilter.Exception import ValidationError
from flask_inputfilter.Validator import BaseValidator


class DateRangeValidator(BaseValidator):
    """
    Validator that checks if a date is within a specific range.
    """

    __slots__ = ("min_date", "max_date", "error_message")

    def __init__(
        self,
        min_date: Optional[Union[str, date, datetime]] = None,
        max_date: Optional[Union[str, date, datetime]] = None,
        error_message: Optional[str] = None,
    ) -> None:
        self.min_date = min_date
        self.max_date = max_date
        self.error_message = error_message

    def validate(self, value: Any) -> None:
        value_date = self.__parse_date(value)
        min_date = self.__parse_date(self.min_date) if self.min_date else None
        max_date = self.__parse_date(self.max_date) if self.max_date else None

        if (min_date and value_date < min_date) or (
            max_date and value_date > max_date
        ):
            raise ValidationError(
                self.error_message
                or f"Date '{value}' is not in the range from "
                f"'{self.min_date}' to '{self.max_date}'."
            )

    @staticmethod
    def __parse_date(value: Any) -> datetime:
        """
        Converts a value to a datetime object.
        Supports ISO 8601 formatted strings and datetime objects.
        """

        if isinstance(value, datetime):
            return value

        elif isinstance(value, str):
            try:
                return datetime.fromisoformat(value)

            except ValueError:
                raise ValidationError(f"Invalid ISO 8601 format '{value}'.")

        elif isinstance(value, date):
            return datetime.combine(value, datetime.min.time())

        raise ValidationError(
            f"Unsupported type for past date validation '{type(value)}'."
        )
