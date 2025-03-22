import json
import re
from collections.abc import Iterator
from pathlib import Path

import pytest

from fake_excel.fields import ExcelFieldFaker
from fake_excel.generator import ExcelFaker


def test_create_fake_excel(schemas_path: Path) -> None:
    with (schemas_path / "mock-values.json").open("r") as f:
        json_schema = json.load(f)

    excel_faker = ExcelFaker(json_schema)
    iterator = excel_faker.get_fake_records()

    assert isinstance(iterator, Iterator)
    record = next(iterator)

    assert isinstance(record, dict)
    assert all(
        isinstance(key, str) and isinstance(value, str) for key, value in record.items()
    )


def test_incorrect_schema() -> None:
    invalid_field = {"": ""}

    with pytest.raises(ValueError, match=f"Unprocessable field {invalid_field}"):
        _ = ExcelFaker([invalid_field])


@pytest.mark.parametrize(
    "fields",
    [
        [
            {"name": "field1", "type": "text"},
        ],
        [
            {"name": "field1", "type": "text"},
            {"name": "field2", "type": "text"},
        ],
        [
            {"name": "field1", "type": "text"},
            {"name": "field2", "type": "text"},
            {"name": "field3", "type": "text"},
        ],
        [
            {"name": "field1", "type": "text"},
            {"name": "field2", "type": "text"},
            {"name": "field3", "type": "text"},
            {"name": "field4", "type": "text"},
            {"name": "field5", "type": "text"},
        ],
    ],
)
def test_field_parsing(fields: list) -> None:
    excel_faker = ExcelFaker(fields)

    assert isinstance(excel_faker.fields, list)
    assert len(excel_faker.fields) == len(fields)
    assert all(isinstance(field, ExcelFieldFaker) for field in excel_faker.fields)


def test_create_from_file(schemas_path: Path) -> None:
    with (schemas_path / "mock-values.json").open("r") as f:
        json_schema = json.load(f)
    expected_faker = ExcelFaker(json_schema)

    actual_faker = ExcelFaker.from_file(schemas_path / "mock-values.json")

    assert isinstance(actual_faker, ExcelFaker)
    assert actual_faker == expected_faker


def test_excel_faker_equality() -> None:
    fields = [
        {"name": "field1", "type": "text"},
        {"name": "field2", "type": "text"},
        {"name": "field3", "type": "text"},
    ]
    faker1 = ExcelFaker(fields)
    faker2 = ExcelFaker(fields)

    assert faker1 == faker2
    assert faker1 is not faker2
    assert faker1 != "This is not an ExcelFaker instance"


def test_print_excel_faker() -> None:
    fields = [
        {"name": "field1", "type": "text"},
        {"name": "field2", "type": "int"},
        {"name": "field3", "type": "bool"},
    ]
    faker = ExcelFaker(fields)

    expected = re.compile(
        r"ExcelFaker\("
        r"\s+TextFieldFaker \{.*?\}\n"
        r"\s+IntegerFieldFaker \{.*?\}\n"
        r"\s+BooleanFieldFaker \{.*?\}\n"
        r"\)",
    )
    assert re.match(expected, str(faker))
