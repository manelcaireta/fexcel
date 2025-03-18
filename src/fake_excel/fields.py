# flake8: noqa: S311

import random
import sys
from abc import ABC, abstractmethod
from datetime import date, datetime, timezone

from faker import Faker

from fake_excel.constraint import FieldConstraint

fake = Faker()


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
        return f"{self.__class__.__name__}(name={self.name})"

    @classmethod
    def parse_field(
        cls,
        field_name: str,
        field_type: str,
        constraints: dict | None = None,
    ) -> "ExcelFieldFaker":
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
    format_string: str = "To be implemented"

    def get_value(self) -> str:
        return self.random_date().strftime("%Y-%m-%d")

    def random_date(
        self,
        min_value: date | None = None,
        max_value: date | None = None,
    ) -> date:
        if min_value is None:
            min_value = date(1970, 1, 1)
        if max_value is None:
            max_value = datetime.now(timezone.utc).date()
        return fake.date_time_between(min_value, max_value)

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class TimeFieldFaker(ExcelFieldFaker):
    def get_value(self) -> str:
        return fake.time()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class DateTimeFieldFaker(ExcelFieldFaker):
    format_string: str = "To be implemented"

    def get_value(self) -> str:
        return self.random_datetime().isoformat(sep=" ")

    def random_datetime(
        self,
        min_value: datetime | None = None,
        max_value: datetime | None = None,
    ) -> datetime:
        if min_value is None:
            min_value = datetime(1970, 1, 1, 0, 0, 0, 0, timezone.utc)
        if max_value is None:
            max_value = datetime.now(timezone.utc)
        return fake.date_time_between(min_value, max_value)

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class TextFieldFaker(ExcelFieldFaker):
    def get_value(self) -> str:
        return fake.text()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class IntegerFieldFaker(ExcelFieldFaker):
    def get_value(self) -> str:
        return str(self.random_int())

    def random_int(
        self,
        min_value: int | None = None,
        max_value: int | None = None,
    ) -> int:
        if min_value is None:
            min_value = -sys.maxsize - 1
        if max_value is None:
            max_value = sys.maxsize
        return random.randint(min_value, max_value)

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class FloatFieldFaker(ExcelFieldFaker):
    def get_value(self) -> str:
        return str(self.random_float())

    def random_float(
        self,
        min_value: float | None = None,
        max_value: float | None = None,
    ) -> float:
        if min_value is None:
            min_value = -sys.float_info.min
        if max_value is None:
            max_value = sys.float_info.max
        return random.uniform(min_value, max_value)

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


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
