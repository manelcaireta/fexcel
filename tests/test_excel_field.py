import re
from dataclasses import dataclass

import pytest

from fake_excel.field import ExcelFieldFaker


@dataclass
class TestCase:
    name: str
    type: str
    expected_pattern: str
    values: list[str] | None = None


test_cases = [
    TestCase(
        name="name",
        type="NAME",
        expected_pattern=r"^[a-zA-Z \.]{2,}$",
        values=None,
    ),
    TestCase(
        name="age",
        type="INTEGER",
        expected_pattern=r"^[0-9]*$",
        values=None,
    ),
    TestCase(
        name="email",
        type="EMAIL",
        expected_pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        values=None,
    ),
    TestCase(
        name="phone",
        type="PHONE",
        expected_pattern=r"^.*$",
        values=None,
    ),
    TestCase(
        name="date",
        type="DATE",
        expected_pattern=r"^\d{4}-\d{2}-\d{2}$",
        values=None,
    ),
    TestCase(
        name="time",
        type="TIME",
        expected_pattern=r"^\d{2}:\d{2}:\d{2}$",
        values=None,
    ),
    TestCase(
        name="datetime",
        type="DATETIME",
        expected_pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d*)?$",
        values=None,
    ),
    TestCase(
        name="boolean",
        type="BOOLEAN",
        expected_pattern=r"^(True|False)$",
        values=None,
    ),
    TestCase(
        name="float",
        type="FLOAT",
        expected_pattern=r"^[0-9]*(\.[0-9]*)?(e[+-]\d*)?$",
        values=None,
    ),
    TestCase(
        name="enum",
        type="ENUM",
        expected_pattern=r"^(a|b|c)$",
        values=["a", "b", "c"],
    ),
]


@pytest.mark.parametrize("test_table", test_cases * 5)
def test_excel_field_generation(test_table: TestCase) -> None:
    value = ExcelFieldFaker(
        test_table.name,
        test_table.type,
        test_table.values,
    ).get_value()
    expected = re.compile(test_table.expected_pattern)
    assert re.match(expected, value) is not None
