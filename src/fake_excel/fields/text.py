from faker import Faker

from fake_excel.constraint import FieldConstraint
from fake_excel.fields.base import ExcelFieldFaker

fake = Faker()


class TextFieldFaker(ExcelFieldFaker, faker_types=["text", "string"]):
    def get_value(self) -> str:
        return fake.text()

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        return super().parse_constraints(constraints)


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
