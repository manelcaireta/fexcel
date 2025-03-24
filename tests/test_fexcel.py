import json
import re
import types
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import pyexcel as pe
import pytest

from fexcel.fields import FexcelField
from fexcel.generator import Fexcel

try:
    import pyexcel_xlsx  # type: ignore[reportMissingImports]
except ImportError:
    pyexcel_xlsx = None

try:
    import pyexcel_xls  # type: ignore[reportMissingImports]
except ImportError:
    pyexcel_xls = None

try:
    import pyexcel_ods3  # type: ignore[reportMissingImports]
except ImportError:
    pyexcel_ods3 = None

try:
    import pyexcel_io  # type: ignore[reportMissingImports]
except ImportError:
    pyexcel_io = None

try:
    import chardet  # type: ignore[reportMissingImports]
    import pyexcel_io  # type: ignore[reportMissingImports]
except ImportError:
    chardet = None


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


@dataclass
class WriteToFileCase:
    extension: str
    module: types.ModuleType | None


write_to_file_cases = [
    WriteToFileCase(extension="xlsx", module=pyexcel_xlsx),
    WriteToFileCase(extension="xls", module=pyexcel_xls),
    WriteToFileCase(extension="ods", module=pyexcel_ods3),
    WriteToFileCase(extension="csv", module=pyexcel_io),
    WriteToFileCase(extension="tsv", module=pyexcel_io),
    WriteToFileCase(extension="csvz", module=chardet),
    WriteToFileCase(extension="tsvz", module=chardet),
]


@pytest.mark.parametrize("tt", write_to_file_cases)
def test_write_to_file(output_path: Path, tt: WriteToFileCase) -> None:
    if tt.module is None:
        pytest.skip(f"Plugin to handle {tt.extension} is not installed")

    output_file = output_path / f"out.{tt.extension}"

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
        name_columns_by_row=0,
    )
    assert set(sheet.colnames) == {"field1", "field2", "field3"}
