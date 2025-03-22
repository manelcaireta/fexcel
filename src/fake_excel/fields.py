# flake8: noqa: S311

import random
from abc import ABC, abstractmethod
from datetime import date, datetime, timezone

from faker import Faker

from fake_excel.constraint import (
    BooleanConstraint,
    ChoiceConstraint,
    FieldConstraint,
    NumericConstraint,
    TemporalConstraint,
)

fake = Faker()


class ExcelFieldFaker(ABC):
    _fakers: dict[str, type["ExcelFieldFaker"]] = {}  # noqa: RUF012

    def __init__(
        self,
        field_name: str,
        *,
        constraints: dict | None = None,
    ) -> None:
        self.name = field_name
        self.constraints = self.parse_constraints(constraints)

    def __init_subclass__(cls, *, faker_types: str | list[str]) -> None:
        cls.register_subclass(faker_types, cls)
        return super().__init_subclass__()

    @classmethod
    def register_subclass(
        cls,
        faker_types: str | list[str],
        faker_subclass: type["ExcelFieldFaker"],
    ) -> None:
        if isinstance(faker_types, str):
            faker_types = [faker_types]
        for faker_type in faker_types:
            _faker_type = faker_type.lower()
            if _faker_type in cls._fakers:
                msg = f"Field type {_faker_type} already registered"
                raise ValueError(msg)
            cls._fakers[_faker_type.lower()] = faker_subclass

    @classmethod
    def get_faker(cls, faker_type: str) -> type["ExcelFieldFaker"]:
        faker_type = faker_type.lower()
        if faker_type not in cls._fakers:
            msg = f"Unknown field type: {faker_type}"
            raise ValueError(msg)
        return cls._fakers[faker_type]

    @abstractmethod
    def get_value(self) -> str: ...

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
        faker_cls = cls.get_faker(field_type)
        return faker_cls(field_name, constraints=constraints)


class ChoiceFieldFaker(ExcelFieldFaker, faker_types="choice"):
    constraints: ChoiceConstraint

    def get_value(self) -> str:
        choice = random.choices(
            population=self.constraints.allowed_values,
            weights=self.constraints.probabilities,
        )
        return choice[0]

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        if not isinstance(constraints, dict):
            return ChoiceConstraint()
        return ChoiceConstraint(
            allowed_values=constraints.get("allowed_values"),
            probabilities=constraints.get("probabilities"),
        )


class NameFieldFaker(ExcelFieldFaker, faker_types="name"):
    def get_value(self) -> str:
        return fake.name()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class EmailFieldFaker(ExcelFieldFaker, faker_types="email"):
    def get_value(self) -> str:
        return fake.email()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class PhoneFieldFaker(ExcelFieldFaker, faker_types="phone"):
    def get_value(self) -> str:
        return fake.phone_number()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class AddressFieldFaker(ExcelFieldFaker, faker_types="address"):
    def get_value(self) -> str:
        return fake.address()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class DateFieldFaker(ExcelFieldFaker, faker_types="date"):
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


class TimeFieldFaker(ExcelFieldFaker, faker_types="time"):
    def get_value(self) -> str:
        return fake.time()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class DateTimeFieldFaker(ExcelFieldFaker, faker_types=["datetime", "timestamp"]):
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


class TextFieldFaker(ExcelFieldFaker, faker_types=["text", "string"]):
    def get_value(self) -> str:
        return fake.text()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class IntegerFieldFaker(ExcelFieldFaker, faker_types=["int", "integer"]):
    constraints: NumericConstraint

    def get_value(self) -> str:
        return str(int(self.constraints.rng()))

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        if not isinstance(constraints, dict):
            return NumericConstraint()
        return NumericConstraint(
            distribution=constraints.get("distribution"),
            min_value=constraints.get("min_value"),
            max_value=constraints.get("max_value"),
            mean=constraints.get("mean"),
            std=constraints.get("std"),
        )


class FloatFieldFaker(ExcelFieldFaker, faker_types=["float", "double"]):
    constraints: NumericConstraint

    def get_value(self) -> str:
        return str(self.constraints.rng())

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        if not isinstance(constraints, dict):
            return NumericConstraint()
        return NumericConstraint(
            distribution=constraints.get("distribution"),
            min_value=constraints.get("min_value"),
            max_value=constraints.get("max_value"),
            mean=constraints.get("mean"),
            std=constraints.get("std"),
        )


class BooleanFieldFaker(ExcelFieldFaker, faker_types=["bool", "boolean"]):
    constraints: BooleanConstraint

    def get_value(self) -> str:
        return str(fake.boolean(int(self.constraints.probability * 100)))

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        if not isinstance(constraints, dict):
            return BooleanConstraint()
        return BooleanConstraint(probability=constraints.get("probability", 0.5))


class URLFieldFaker(ExcelFieldFaker, faker_types="url"):
    def get_value(self) -> str:
        return fake.url()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class IPv4FieldFaker(ExcelFieldFaker, faker_types="ipv4"):
    def get_value(self) -> str:
        return fake.ipv4()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class IPv6FieldFaker(ExcelFieldFaker, faker_types="ipv6"):
    def get_value(self) -> str:
        return fake.ipv6()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class UUIDFieldFaker(ExcelFieldFaker, faker_types="uuid"):
    def get_value(self) -> str:
        return fake.uuid4()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


class LocationFieldFaker(ExcelFieldFaker, faker_types="location"):
    def get_value(self) -> str:
        return fake.locale()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)
