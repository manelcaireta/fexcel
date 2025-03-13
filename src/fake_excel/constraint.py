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

    def __init__(self, allowed_values: list | None = None) -> None:
        self.allowed_values = allowed_values

    def __str__(self) -> str:
        return f"{{allowed_values={self.allowed_values}}}"


class NumericConstraint(FieldConstraint):
    """
    Numerical constraint. It represents constraints for float or int types.
    """

    def __init__(
        self,
        min_value: float | Iterator[float | None] | None = None,
        max_value: float | Iterator[float | None] | None = None,
        allowed_values: list[float] | None = None,
    ) -> None:
        if isinstance(min_value, (int, float, NoneType)):
            min_value = repeat(min_value)
        if isinstance(max_value, (int, float, NoneType)):
            max_value = repeat(max_value)
        self._min_value = min_value
        self._max_value = max_value
        super().__init__(allowed_values)

    @property
    def min_value(self) -> float | None:
        return next(self._min_value)

    @property
    def max_value(self) -> float | None:
        return next(self._max_value)

    def __str__(self) -> str:
        return (
            f"{{allowed_values={self.allowed_values} "
            f"min_value={self.min_value} "
            f"max_value={self.max_value}}}"
        )


class TemporalConstraint(FieldConstraint):
    """
    Temporal constraint. It represents constraints for date or datetime types.
    """

    def __init__(
        self,
        min_value: str | datetime | Iterator[datetime | None] | None = None,
        max_value: str | datetime | Iterator[datetime | None] | None = None,
        allowed_values: list[str] | None = None,
    ) -> None:
        if isinstance(min_value, str):
            min_value = datetime.fromisoformat(min_value)
        if isinstance(min_value, (datetime, date, NoneType)):
            min_value = repeat(min_value)
        if isinstance(max_value, str):
            max_value = datetime.fromisoformat(max_value)
        if isinstance(max_value, (datetime, date, NoneType)):
            max_value = repeat(max_value)
        self._min_value = min_value
        self._max_value = max_value
        super().__init__(allowed_values)

    @property
    def min_value(self) -> datetime | None:
        return next(self._min_value)

    @property
    def max_value(self) -> datetime | None:
        return next(self._max_value)

    def __str__(self) -> str:
        return (
            f"{{allowed_values={self.allowed_values} "
            f"min_value={self.min_value} "
            f"max_value={self.max_value}}}"
        )
