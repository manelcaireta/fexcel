import json
import re
from collections.abc import Iterator
from pathlib import Path

import pyexcel as pe
import pytest

from fexcel.fields import FexcelField
from fexcel.generator import Fexcel


def test_create_fake_excel(input_path: Path) -> None:
    with (input_path / "mock-values.json").open("r") as f:
        json_schema = json.load(f)

    excel_faker = Fexcel(json_schema)
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
        _ = Fexcel([invalid_field])


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
    excel_faker = Fexcel(fields)

    assert isinstance(excel_faker.fields, list)
    assert len(excel_faker.fields) == len(fields)
    assert all(isinstance(field, FexcelField) for field in excel_faker.fields)


def test_create_from_file(input_path: Path) -> None:
    with (input_path / "mock-values.json").open("r") as f:
        json_schema = json.load(f)
    expected_faker = Fexcel(json_schema)

    actual_faker = Fexcel.from_file(input_path / "mock-values.json")

    assert isinstance(actual_faker, Fexcel)
    assert actual_faker == expected_faker


def test_excel_faker_equality() -> None:
    fields = [
        {"name": "field1", "type": "text"},
        {"name": "field2", "type": "text"},
        {"name": "field3", "type": "text"},
    ]
    faker1 = Fexcel(fields)
    faker2 = Fexcel(fields)

    assert faker1 == faker2
    assert faker1 is not faker2
    assert faker1 != "This is not an ExcelFaker instance"


def test_print_excel_faker() -> None:
    fields = [
        {"name": "field1", "type": "text"},
        {"name": "field2", "type": "int"},
        {"name": "field3", "type": "bool"},
    ]
    faker = Fexcel(fields)

    expected = re.compile(
        r"ExcelFaker\("
        r"\s+TextFieldFaker \{.*?\}\n"
        r"\s+IntegerFieldFaker \{.*?\}\n"
        r"\s+BooleanFieldFaker \{.*?\}\n"
        r"\)",
    )
    assert re.match(expected, str(faker))


def test_write_to_file(output_path: Path) -> None:
    output_file = output_path / "out.xlsx"
    if output_file.exists():
        output_file.unlink()

    fields = [
        {"name": "field1", "type": "text"},
        {"name": "field2", "type": "int"},
        {"name": "field3", "type": "bool"},
    ]
    faker = Fexcel(fields)
    faker.write_to_file(output_file)

    assert output_file.exists()
    assert output_file.is_file()

    sheet = pe.get_sheet(
        file_name=str(output_file),
        sheet_name="Sheet1",
        name_columns_by_row=0,
    )
    assert set(sheet.colnames) == {"field1", "field2", "field3"}
