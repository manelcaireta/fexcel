# flake8: noqa: E501, DTZ007

from datetime import datetime, timezone

import pytest

from fexcel.fields import (
    DateFieldFaker,
    DateTimeFieldFaker,
    FexcelField,
)

# fmt: off
temporal_field_sample = [
    FexcelField.parse_field("DateField", "date"),
    FexcelField.parse_field("DateField", "date", start_date="2023-01-01"),
    FexcelField.parse_field("DateField", "date", end_date="2023-12-31"),
    FexcelField.parse_field("DateField", "date", start_date="2023-01-01", end_date="2023-12-31"),
    FexcelField.parse_field("DateTimeField", "datetime"),
    FexcelField.parse_field("DateTimeField", "datetime", start_date="2023-01-01"),
    FexcelField.parse_field("DateTimeField", "datetime", end_date="2023-12-31"),
    FexcelField.parse_field("DateTimeField", "datetime", start_date="2023-01-01", end_date="2023-12-31"),
]
# fmt: on


@pytest.mark.parametrize("field", temporal_field_sample)
def test_temporal_constraint(field: FexcelField) -> None:
    assert isinstance(field, DateFieldFaker | DateTimeFieldFaker)

    if field.start_date is not None:
        got = datetime.strptime(field.get_value(), field.format_string)
        assert got.astimezone(timezone.utc) >= field.start_date.astimezone(timezone.utc)
    if field.end_date is not None:
        got = datetime.strptime(field.get_value(), field.format_string)
        assert got.astimezone(timezone.utc) <= field.end_date.astimezone(timezone.utc)


def test_invalid_temporal_constraint() -> None:
    with pytest.raises(ValueError, match=r"Invalid 'start_date'"):
        FexcelField.parse_field("DateField", "datetime", start_date="FAIL")
