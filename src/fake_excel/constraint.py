from datetime import date, datetime
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
    ) -> None:
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date)
        if isinstance(start_date, (datetime, date, NoneType)):
            start_date = repeat(start_date)
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date)
        if isinstance(end_date, (datetime, date, NoneType)):
            end_date = repeat(end_date)
        self.start_date = start_date
        self.end_date = end_date
        super().__init__()
