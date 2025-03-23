import random
from functools import partial

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

        super().__init__(field_name)

    def get_value(self) -> str:
        return str(self.rng())

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


# NOTE: If Python allows `int` to be treated as a `float` then I will too
class IntegerFieldFaker(FloatFieldFaker, faker_types=["int", "integer"]):
    def get_value(self) -> str:
        return str(int(self.rng()))
