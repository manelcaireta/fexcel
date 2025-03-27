# flake8: noqa: E501, DTZ007


import pytest

from fexcel.fields import (
    FexcelField,
)

# SIMPLE CONSTRAINT TESTS


def test_boolean_distributions() -> None:
    max_range = 100

    field_faker = FexcelField.parse_field(
        field_name="BooleanField",
        field_type="bool",
        probability=0,
    )
    random_sample = [field_faker.get_value() for _ in range(max_range)]
    assert random_sample.count(str(True)) == 0
    assert random_sample.count(str(False)) == max_range

    field_faker = FexcelField.parse_field(
        field_name="BooleanField",
        field_type="bool",
        probability=1,
    )
    random_sample = [field_faker.get_value() for _ in range(max_range)]
    assert random_sample.count(str(True)) == max_range
    assert random_sample.count(str(False)) == 0

    field_faker = FexcelField.parse_field(
        field_name="BooleanField",
        field_type="bool",
        probability=0.5,
    )
    random_sample = [field_faker.get_value() for _ in range(max_range)]
    assert random_sample.count(str(True)) >= 0
    assert random_sample.count(str(True)) <= max_range
    assert random_sample.count(str(False)) >= 0
    assert random_sample.count(str(False)) <= max_range


def test_invalid_boolean_distribution() -> None:
    with pytest.raises(
        ValueError,
        match=r"Probability must be between 0 and 1, got .*",
    ):
        FexcelField.parse_field(
            field_name="BooleanField",
            field_type="bool",
            probability=-1,
        )
    with pytest.raises(
        ValueError,
        match=r"Probability must be between 0 and 1, got .*",
    ):
        FexcelField.parse_field(
            field_name="BooleanField",
            field_type="bool",
            probability=2,
        )
