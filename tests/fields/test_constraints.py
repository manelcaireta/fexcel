# flake8: noqa: E501, DTZ007

from datetime import datetime

import pytest
from fake_excel.constraint import NumericConstraint, TemporalConstraint
from fake_excel.fields import DateFieldFaker, DateTimeFieldFaker, ExcelFieldFaker

# fmt: off
numeric_field_sample = [
    ExcelFieldFaker.parse_field("IntegerField", "int"),
    ExcelFieldFaker.parse_field("IntegerField", "int", {"min_value": 0}),
    ExcelFieldFaker.parse_field("IntegerField", "int", {"max_value": 100}),
    ExcelFieldFaker.parse_field("IntegerField", "int", {"min_value": 0, "max_value": 100}),
    ExcelFieldFaker.parse_field("FloatingPointField", "float"),
    ExcelFieldFaker.parse_field("FloatingPointField", "float", {"min_value": 0}),
    ExcelFieldFaker.parse_field("FloatingPointField", "float", {"max_value": 100.0}),
    ExcelFieldFaker.parse_field("FloatingPointField", "float", {"min_value": 0, "max_value": 100}),
]
# fmt: on


@pytest.mark.parametrize("field", numeric_field_sample)
def test_numeric_constraint(field: ExcelFieldFaker) -> None:
    assert isinstance(field.constraints, NumericConstraint)

    if field.constraints.min_value is not None:
        assert float(field.get_value()) >= field.constraints.min_value
    if field.constraints.max_value is not None:
        assert float(field.get_value()) <= field.constraints.max_value


# fmt: off
temporal_field_sample = [
    ExcelFieldFaker.parse_field("DateField", "date"),
    ExcelFieldFaker.parse_field("DateField", "date", {"start_date": "2023-01-01"}),
    ExcelFieldFaker.parse_field("DateField", "date", {"end_date": "2023-12-31"}),
    ExcelFieldFaker.parse_field("DateField", "date", {"start_date": "2023-01-01", "end_date": "2023-12-31"}),
    ExcelFieldFaker.parse_field("DateTimeField", "datetime"),
    ExcelFieldFaker.parse_field("DateTimeField", "datetime", {"start_date": "2023-01-01"}),
    ExcelFieldFaker.parse_field("DateTimeField", "datetime", {"end_date": "2023-12-31"}),
    ExcelFieldFaker.parse_field("DateTimeField", "datetime", {"start_date": "2023-01-01", "end_date": "2023-12-31"}),
]
# fmt: on


@pytest.mark.parametrize("field", temporal_field_sample)
def test_temporal_constraint(field: ExcelFieldFaker) -> None:
    assert isinstance(field, DateFieldFaker | DateTimeFieldFaker)
    assert isinstance(field.constraints, TemporalConstraint)

    if field.constraints.start_date is not None:
        assert (
            datetime.strptime(field.get_value(), field.format_string)
            >= field.constraints.start_date
        )
    if field.constraints.end_date is not None:
        assert (
            datetime.strptime(field.get_value(), field.format_string)
            <= field.constraints.end_date
        )


def test_choice_constraint() -> None:
    allowed_values = ["A", "B", "C"]

    field_faker = ExcelFieldFaker.parse_field(
        field_name="ChoiceField",
        field_type="choice",
        constraints={"allowed_values": allowed_values},
    )

    for _ in range(100):
        assert field_faker.get_value() in allowed_values
