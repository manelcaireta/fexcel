import random
import sys
import typing
from collections.abc import Callable
from functools import partial

from faker import Faker

from fake_excel.constraint import FieldConstraint, NumericConstraint

fake = Faker()


def random_float(
    min_value: float | None = None,
    max_value: float | None = None,
) -> float:
    if min_value is None:
        min_value = -sys.float_info.min
    if max_value is None:
        max_value = sys.float_info.max
    return random.uniform(min_value, max_value)  # noqa: S311


def random_int(
    min_value: int | None = None,
    max_value: int | None = None,
) -> int:
    if min_value is None:
        min_value = -sys.maxsize - 1
    if max_value is None:
        max_value = sys.maxsize
    return random.randint(min_value, max_value)  # noqa: S311


type_to_generator = {
    "name": fake.name,
    "email": fake.email,
    "phone": fake.phone_number,
    "address": fake.address,
    "date": fake.date,
    "time": fake.time,
    "datetime": fake.date_time,
    "text": fake.text,
    "int": random_int,
    "integer": random_int,
    "float": random_float,
    "boolean": fake.boolean,
    "url": fake.url,
    "ipv4": fake.ipv4,
    "ipv6": fake.ipv6,
    "uuid": fake.uuid4,
    "location": fake.locale,
}


class ExcelFieldFaker:
    def __init__(
        self,
        field_name: str,
        field_type: str,
        field_constraints: FieldConstraint,
    ) -> None:
        self.name = field_name
        self._type = field_type.lower()
        self._value_creator = None
        self._constraints = field_constraints
        self._last_value = None

    def get_value(self) -> str:
        if self._value_creator is None:
            self._value_creator = self._get_value_creator()
        return str(self._value_creator())

    def _get_value_creator(self) -> Callable[[], str | float]:
        if self._constraints.allowed_values is not None:
            return self._value_creator_from_allowed_values()
        if isinstance(self._constraints, NumericConstraint):
            return self._value_creator_from_range()
        return type_to_generator.get(self._type, lambda *_args, **_kwargs: "NULL")

    def _value_creator_from_allowed_values(self) -> Callable[[], str]:
        values = typing.cast(list, self._constraints.allowed_values).copy()
        return lambda: fake.random_element(values)

    def _value_creator_from_range(self) -> Callable[[], str | float]:
        self._constraints = typing.cast(NumericConstraint, self._constraints)

        func = type_to_generator.get(self._type, random_int)
        if self._constraints.min_value is not None:
            func = partial(func, min_value=self._constraints.min_value)
        if self._constraints.max_value is not None:
            func = partial(func, max_value=self._constraints.max_value)
        return func

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, ExcelFieldFaker):
            return False
        return self.name == value.name and self._type == value._type

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(name={self.name} "
            f"type={self._type} "
            f"constraints={self._constraints})"
        )
