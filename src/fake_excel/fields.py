# flake8: noqa: S311

import random
from abc import ABC, abstractmethod
from datetime import date, datetime, timezone

from faker import Faker

from fake_excel.constraint import (
    ChoiceConstraint,
    FieldConstraint,
    NumericConstraint,
    TemporalConstraint,
)

fake = Faker()

INFINITY = 1e30
"""
A very large number but not large enough to mess with RNGs.

Using something like `sys.float_info.max` or `math.inf` can make the RNGs respond
with `math.inf`.
"""


class ExcelFieldFaker(ABC):
    def __init__(
        self,
        field_name: str,
        *,
        constraints: dict | None = None,
    ) -> None:
        self.name = field_name
        self.constraints = self.parse_constraints(constraints)

    @abstractmethod
    def get_value(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return None

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, self.__class__):
            return False
        return self.name == value.name

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(name={self.name} "
            f"constraints={self.constraints})"
        )

    @classmethod
    def parse_field(
        cls,
        field_name: str,
        field_type: str,
        constraints: dict | None = None,
    ) -> "ExcelFieldFaker":
        if constraints and "allowed_values" in constraints:
            return ChoiceFieldFaker(
                field_name=field_name,
                constraints=constraints,
            )

        field_fakers: dict[str, type[ExcelFieldFaker]] = {
            "name": NameFieldFaker,
            "email": EmailFieldFaker,
            "phone": PhoneFieldFaker,
            "address": AddressFieldFaker,
            "date": DateFieldFaker,
            "time": TimeFieldFaker,
            "datetime": DateTimeFieldFaker,
            "text": TextFieldFaker,
            "int": IntegerFieldFaker,
            "integer": IntegerFieldFaker,
            "float": FloatFieldFaker,
            "bool": BooleanFieldFaker,
            "boolean": BooleanFieldFaker,
            "url": URLFieldFaker,
            "uuid": UUIDFieldFaker,
            "ipv4": IPv4FieldFaker,
            "ipv6": IPv6FieldFaker,
            "location": LocationFieldFaker,
        }

        field_type_lower = field_type.lower()
        if field_type_lower not in field_fakers:
            msg = f"Unknown field type: {field_type}"
            raise ValueError(msg)

        return field_fakers[field_type_lower](field_name, constraints=constraints)


class ChoiceFieldFaker(ExcelFieldFaker):
    constraints: ChoiceConstraint

    def get_value(self) -> str:
        return random.choice(self.constraints.allowed_values)

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        if not isinstance(constraints, dict):
            return ChoiceConstraint()
        return ChoiceConstraint(allowed_values=constraints.get("allowed_values"))


class NameFieldFaker(ExcelFieldFaker):
    def get_value(self) -> str:
        return fake.name()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class EmailFieldFaker(ExcelFieldFaker):
    def get_value(self) -> str:
        return fake.email()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class PhoneFieldFaker(ExcelFieldFaker):
    def get_value(self) -> str:
        return fake.phone_number()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class AddressFieldFaker(ExcelFieldFaker):
    def get_value(self) -> str:
        return fake.address()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class DateFieldFaker(ExcelFieldFaker):
    constraints: TemporalConstraint

    def get_value(self) -> str:
        return self.random_date().strftime("%Y-%m-%d")

    def random_date(self) -> date:
        start_date = self.constraints.start_date or date(1970, 1, 1)
        end_date = self.constraints.end_date or datetime.now(timezone.utc).date()
        return fake.date_time_between(start_date, end_date)

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        if not isinstance(constraints, dict):
            return TemporalConstraint()
        return TemporalConstraint(
            start_date=constraints.get("start_date"),
            end_date=constraints.get("end_date"),
            format_string=constraints.get("format_string", "%Y-%m-%d"),
        )


class TimeFieldFaker(ExcelFieldFaker):
    def get_value(self) -> str:
        return fake.time()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class DateTimeFieldFaker(ExcelFieldFaker):
    constraints: TemporalConstraint

    def get_value(self) -> str:
        return self.random_datetime().strftime(self.constraints.format_string)

    def random_datetime(self) -> datetime:
        epoch = datetime(1970, 1, 1, 0, 0, 0, 0, timezone.utc)
        start_value = self.constraints.start_date or epoch
        end_value = self.constraints.end_date or datetime.now(timezone.utc)
        return fake.date_time_between(start_value, end_value)

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        if not isinstance(constraints, dict):
            return TemporalConstraint(format_string="%Y-%m-%d %H:%M:%S")
        return TemporalConstraint(
            start_date=constraints.get("start_date"),
            end_date=constraints.get("end_date"),
            format_string=constraints.get("format_string", "%Y-%m-%d %H:%M:%S"),
        )


class TextFieldFaker(ExcelFieldFaker):
    def get_value(self) -> str:
        return fake.text()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class IntegerFieldFaker(ExcelFieldFaker):
    constraints: NumericConstraint

    def get_value(self) -> str:
        return str(self.random_int())

    def random_int(self) -> int:
        min_value = self.constraints.min_value
        if min_value is None:
            min_value = -INFINITY
        max_value = self.constraints.max_value
        if max_value is None:
            max_value = INFINITY
        return random.randint(int(min_value), int(max_value))

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        if not isinstance(constraints, dict):
            return NumericConstraint()
        return NumericConstraint(
            constraints.get("min_value"),
            constraints.get("max_value"),
        )


class FloatFieldFaker(ExcelFieldFaker):
    constraints: NumericConstraint

    def get_value(self) -> str:
        return str(self.random_float())

    def random_float(
        self,
        min_value: float | None = None,
        max_value: float | None = None,
    ) -> float:
        min_value = self.constraints.min_value
        if min_value is None:
            min_value = -INFINITY
        max_value = self.constraints.max_value
        if max_value is None:
            max_value = INFINITY
        return random.uniform(min_value, max_value)

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        if not isinstance(constraints, dict):
            return NumericConstraint()
        return NumericConstraint(
            constraints.get("min_value"),
            constraints.get("max_value"),
        )


class BooleanFieldFaker(ExcelFieldFaker):
    def get_value(self) -> str:
        return str(fake.boolean())

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class URLFieldFaker(ExcelFieldFaker):
    def get_value(self) -> str:
        return fake.url()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class IPv4FieldFaker(ExcelFieldFaker):
    def get_value(self) -> str:
        return fake.ipv4()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class IPv6FieldFaker(ExcelFieldFaker):
    def get_value(self) -> str:
        return fake.ipv6()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class UUIDFieldFaker(ExcelFieldFaker):
    def get_value(self) -> str:
        return fake.uuid4()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class LocationFieldFaker(ExcelFieldFaker):
    def get_value(self) -> str:
        return fake.locale()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)
