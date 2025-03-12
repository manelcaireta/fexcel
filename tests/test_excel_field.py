import re
from dataclasses import dataclass

import pytest

from fake_excel.constraint import FieldConstraint, NumericConstraint
from fake_excel.field import ExcelFieldFaker


@dataclass
class TestCase:
    name: str
    type: str
    constraints: FieldConstraint
    expected_pattern: str


test_cases = [
    TestCase(
        name="name",
        type="NAME",
        constraints=FieldConstraint(),
        expected_pattern=r"^[a-zA-Z \.]{2,}$",
    ),
    TestCase(
        name="age",
        type="INTEGER",
        constraints=NumericConstraint(min_value=0, max_value=100),
        expected_pattern=r"^[-+]?[0-9]*$",
    ),
    TestCase(
        name="email",
        type="EMAIL",
        constraints=FieldConstraint(),
        expected_pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    ),
    TestCase(
        name="phone",
        type="PHONE",
        constraints=FieldConstraint(),
        expected_pattern=r"^.*$",
    ),
    TestCase(
        name="date",
        type="DATE",
        constraints=FieldConstraint(),
        expected_pattern=r"^\d{4}-\d{2}-\d{2}$",
    ),
    TestCase(
        name="time",
        type="TIME",
        constraints=FieldConstraint(),
        expected_pattern=r"^\d{2}:\d{2}:\d{2}$",
    ),
    TestCase(
        name="datetime",
        type="DATETIME",
        constraints=FieldConstraint(),
        expected_pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(\.\d*)?$",
    ),
    TestCase(
        name="boolean",
        type="BOOLEAN",
        constraints=FieldConstraint(),
        expected_pattern=r"^(True|False)$",
    ),
    TestCase(
        name="float",
        type="FLOAT",
        constraints=FieldConstraint(),
        expected_pattern=r"^[-+]?[0-9]*(\.[0-9]*)?(e[+-]\d*)?$",
    ),
    TestCase(
        name="enum",
        type="TEXT",
        constraints=FieldConstraint(["a", "b", "c"]),
        expected_pattern=r"^(a|b|c)$",
    ),
]


@pytest.mark.parametrize("test_table", test_cases * 5)
def test_excel_field_generation(test_table: TestCase) -> None:
    value = ExcelFieldFaker(
        test_table.name,
        test_table.type,
        test_table.constraints,
    ).get_value()
    expected = re.compile(test_table.expected_pattern)

    assert re.match(expected, value) is not None

    if test_table.constraints.allowed_values is not None:
        assert value in test_table.constraints.allowed_values

    if isinstance(test_table.constraints, NumericConstraint):
        if test_table.constraints.min_value is not None:
            assert test_table.constraints.min_value <= int(value)
        if test_table.constraints.max_value is not None:
            assert int(value) <= test_table.constraints.max_value


def test_excel_fields_equality() -> None:
    faker = ExcelFieldFaker("Test", "INTEGER", FieldConstraint())

    assert faker == ExcelFieldFaker("Test", "INTEGER", FieldConstraint())
    assert faker is not ExcelFieldFaker("Test", "INTEGER", FieldConstraint())
    assert faker != ExcelFieldFaker("Test", "TEXT", FieldConstraint())
    assert faker != "Not a FieldFaker instance"
