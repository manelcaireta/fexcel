from datetime import date, datetime, timezone
from itertools import repeat
from types import NoneType
from typing import Iterator


class FieldConstraint:
    """
    Base constraint to apply to a Field.

    It only contains the `allowed_values` option
    which is shared across all posible types.
    """

    def __str__(self) -> str:
        ret = "{"
        ret += " ".join(f"{k}={v}" for k, v in self.__dict__.items())
        ret += "}"
        return ret


class ChoiceConstraint(FieldConstraint):
    """
    Choice constraint. It represents a list of values that can appear in the field.
    """

    def __init__(self, allowed_values: list[str] | None = None) -> None:
        self.allowed_values = allowed_values or ["NULL"]
        super().__init__()

class NumericConstraint(FieldConstraint):
    """
    Numerical constraint. It represents constraints for float or int types.
    """

    def __init__(
        self,
        min_value: float | Iterator[float | None] | None = None,
        max_value: float | Iterator[float | None] | None = None,
    ) -> None:
        if isinstance(min_value, (int, float, NoneType)):
            min_value = repeat(min_value)
        if isinstance(max_value, (int, float, NoneType)):
            max_value = repeat(max_value)
        self._min_value = min_value
        self._max_value = max_value
        super().__init__()

    @property
    def min_value(self) -> float | None:
        return next(self._min_value)

    @property
    def max_value(self) -> float | None:
        return next(self._max_value)


class TemporalConstraint(FieldConstraint):
    """
    Temporal constraint. It represents constraints for date or datetime types.
    """

    def __init__(
        self,
        start_date: str | datetime | Iterator[datetime | None] | None = None,
        end_date: str | datetime | Iterator[datetime | None] | None = None,
        format_string: str | None = None,
    ) -> None:
        self.format_string = format_string or "%Y-%m-%d"

        if isinstance(start_date, str):
            start_date = self._try_parse_datetime(start_date)
        if isinstance(start_date, (datetime, date, NoneType)):
            start_date = repeat(start_date)
        self._start_date = start_date

        if isinstance(end_date, str):
            end_date = self._try_parse_datetime(end_date)
        if isinstance(end_date, (datetime, date, NoneType)):
            end_date = repeat(end_date)
        self._end_date = end_date

        super().__init__()

    @property
    def start_date(self) -> datetime | None:
        return next(self._start_date)

    @property
    def end_date(self) -> datetime | None:
        return next(self._end_date)

    def _try_parse_datetime(self, value: str) -> datetime | None:
        try:
            return datetime.strptime(value, self.format_string).astimezone(timezone.utc)
        except ValueError:
            return datetime.fromisoformat(value)
