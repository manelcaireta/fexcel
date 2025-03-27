import random
from functools import partial
from typing import Any

from faker import Faker

from fexcel.fields.base import FexcelField

fake = Faker()
INFINITY = 1e30
"""
A very large number but not large enough to mess with RNGs.

Using something like `sys.float_info.max` or `math.inf` can make the RNGs respond
with `math.inf`.
"""


class FloatFieldFaker(FexcelField, faker_types="float"):
    INTERVAL_DISTRIBUTIONS = ("uniform",)
    EXPONENTIAL_DISTRIBUTIONS = ("normal", "gaussian", "lognormal")

    def __init__(  # noqa: PLR0913
        self,
        field_name: str,
        *,
        min_value: float | None = None,
        max_value: float | None = None,
        mean: float | None = None,
        std: float | None = None,
        distribution: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(field_name, **kwargs)

        self.is_min_max = bool(min_value is not None or max_value is not None)
        self.is_mean_std = bool(mean is not None or std is not None)
        self.distribution = distribution or "uniform"

        self.min_value = self._ensure_float(min_value, "min_value", -INFINITY)
        self.max_value = self._ensure_float(max_value, "max_value", INFINITY)
        self.mean = self._ensure_float(mean, "mean", 0)
        self.std = self._ensure_float(std, "std", 1)

        self._raise_if_invalid_combination()
        self._resolve_rng()

    @staticmethod
    def _ensure_float(
        value: float | str | None,
        var_name: str,
        default: float,
    ) -> float:
        if value is None:
            return default
        if not isinstance(value, float):
            try:
                return float(value)
            except (ValueError, TypeError) as err:
                msg = f"Invalid '{var_name}': Unable to convert '{value}' to float"
                raise ValueError(msg) from err
        return value

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
                msg = f"Invalid distribution: {self.distribution} for field {self.name}"
                raise ValueError(msg)

    def get_value(self) -> str:
        return str(self.rng())


# NOTE: If Python allows `int` to be treated as a `float` then I will too
class IntegerFieldFaker(FloatFieldFaker, faker_types=["int", "integer"]):
    def get_value(self) -> str:
        return str(int(self.rng()))
