# flake8: noqa: S311

import random
from copy import deepcopy
from datetime import date, datetime, timezone
from functools import partial
from itertools import repeat
from types import NoneType
from typing import Iterator

INFINITY = 1e30
"""
A very large number but not large enough to mess with RNGs.

Using something like `sys.float_info.max` or `math.inf` can make the RNGs respond
with `math.inf`.
"""


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

    def __init__(
        self,
        allowed_values: list[str] | None = None,
        probabilities: list[float] | None = None,
    ) -> None:
        self.allowed_values = allowed_values or ["NULL"]
        if not probabilities:
            probabilities = [1 / len(self.allowed_values)] * len(self.allowed_values)
        self.probabilities = self._parse_probabilities(probabilities)
        super().__init__()

    def _parse_probabilities(self, original_probabilities: list[float]) -> list[float]:
        probabilities = deepcopy(original_probabilities)
        if len(probabilities) <= len(self.allowed_values):
            remaining_probability_space = 1 - sum(probabilities)
            remaining_observations = len(probabilities) - len(self.allowed_values)
            probabilities.extend(
                remaining_probability_space / remaining_observations
                for _ in range(remaining_observations)
            )

        if len(probabilities) > len(self.allowed_values):
            msg = (
                f"Probabilities must have the same length as 'allowed_values' "
                f"or less, got length of probabilities is {len(probabilities)} when "
                f"length of 'allowed_values' is {len(self.allowed_values)}"
            )
            raise ValueError(msg)

        if any(p < 0 for p in probabilities):
            msg = f"Probabilities must be positive, got {probabilities}"
            raise ValueError(msg)

        if sum(probabilities) != 1:
            msg = f"Probabilities must sum up to 1, got {sum(probabilities)}"
            raise ValueError(msg)

        return probabilities


class NumericConstraint(FieldConstraint):
    """
    Numerical constraint. It represents constraints for float or int types.
    """

    INTERVAL_DISTRIBUTIONS = ("uniform",)
    EXPONENTIAL_DISTRIBUTIONS = ("normal", "gaussian", "lognormal")

    def __init__(
        self,
        *,
        min_value: float | None = None,
        max_value: float | None = None,
        mean: float | None = None,
        std: float | None = None,
        distribution: str | None = None,
    ) -> None:
        self.is_min_max = bool(min_value is not None or max_value is not None)
        self.is_mean_std = bool(mean is not None or std is not None)
        self.distribution = distribution or "uniform"
        self.min_value = min_value if min_value is not None else -INFINITY
        self.max_value = max_value if max_value is not None else INFINITY
        self.mean = mean if mean is not None else 0
        self.std = std if std is not None else 1

        self._raise_if_invalid_combination()
        self._resolve_rng()

        super().__init__()

    def _raise_if_invalid_combination(self) -> None:
        if (self.is_min_max) and (self.is_mean_std):
            msg = "Cannot specify both min_value/max_value and mean/std"
            raise ValueError(msg)

        if (self.is_min_max) and (self.distribution in self.EXPONENTIAL_DISTRIBUTIONS):
            msg = (
                "Cannot specify min_value/max_value with "
                f"{self.distribution} distribution"
            )
            raise ValueError(msg)

        if (self.is_mean_std) and (self.distribution in self.INTERVAL_DISTRIBUTIONS):
            msg = f"Cannot specify mean/std with {self.distribution} distribution"
            raise ValueError(msg)

        if self.min_value > self.max_value:
            msg = "min_value must be less than or equal than max_value"
            raise ValueError(msg)

    def _resolve_rng(self) -> None:
        match self.distribution.lower():
            case "uniform":
                self.rng = partial(random.uniform, self.min_value, self.max_value)
            case "normal":
                self.rng = partial(random.normalvariate, self.mean, self.std)
            case "gaussian":
                self.rng = partial(random.gauss, self.mean, self.std)
            case "lognormal":
                self.rng = partial(random.lognormvariate, self.mean, self.std)
            case _:
                msg = f"Invalid distribution: {self.distribution}"
                raise ValueError(msg)


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


class BooleanConstraint(FieldConstraint):
    """
    Boolean constraint. It represents constraints for boolean types.
    """

    def __init__(self, *, probability: float = 0.5) -> None:
        if probability < 0 or probability > 1:
            msg = f"Probability must be between 0 and 1, got {probability}"
            raise ValueError(msg)
        self.probability = probability
        super().__init__()
