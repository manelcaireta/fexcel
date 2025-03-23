from uuid import uuid4

import pytest

from fexcel.fields import ExcelFieldFaker


def test_field_registration() -> None:
    class MockFieldFaker(ExcelFieldFaker, faker_types="test_field"):
        def get_value(self) -> str:
            return "test_value"

    field_faker = ExcelFieldFaker.parse_field(
        field_name="mock",
        field_type="test_field",
    )

    assert isinstance(field_faker, MockFieldFaker)
    assert field_faker.get_value() == "test_value"


def test_invalid_field_registration() -> None:
    with pytest.raises(TypeError):

        class MockFieldFaker(ExcelFieldFaker): ...  # type: ignore[]


def test_repeated_type_registration() -> None:
    uuid = str(uuid4())

    class MockFieldFaker1(ExcelFieldFaker, faker_types=uuid): ...

    with pytest.raises(ValueError, match=f"Field type {uuid} already registered"):

        class MockFieldFaker2(ExcelFieldFaker, faker_types=uuid): ...
