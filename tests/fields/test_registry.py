from uuid import uuid4

import pytest

from fake_excel.constraint import FieldConstraint
from fake_excel.fields import ExcelFieldFaker


def test_field_registration() -> None:
    class MockFieldFaker(ExcelFieldFaker, faker_types="test_field"):
        def get_value(self) -> str:
            return "test_value"

        def parse_constraints(self, constraints: dict) -> FieldConstraint | None:
            return super().parse_constraints(constraints)

    field_faker = ExcelFieldFaker.parse_field(
        field_name="mock",
        field_type="test_field",
    )

    assert isinstance(field_faker, MockFieldFaker)
    assert field_faker.get_value() == "test_value"
    assert field_faker.parse_constraints({}) is None


def test_invalid_field_registration() -> None:
    with pytest.raises(TypeError):

        class MockFieldFaker(ExcelFieldFaker): ...  # type: ignore[]


def test_repeated_type_registration() -> None:
    uuid = str(uuid4())

    class MockFieldFaker1(ExcelFieldFaker, faker_types=uuid): ...

    with pytest.raises(ValueError, match=f"Field type {uuid} already registered"):

        class MockFieldFaker2(ExcelFieldFaker, faker_types=uuid): ...
