# flake8: noqa: E501, DTZ007

import random
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

import pytest

from fake_excel.constraint import NumericConstraint, TemporalConstraint
from fake_excel.fields import (
    DateFieldFaker,
    DateTimeFieldFaker,
    ExcelFieldFaker,
)

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
        assert datetime.strptime(
            field.get_value(),
            field.constraints.format_string,
        ).astimezone(timezone.utc) >= field.constraints.start_date.astimezone(
            timezone.utc,
        )
    if field.constraints.end_date is not None:
        assert datetime.strptime(
            field.get_value(),
            field.constraints.format_string,
        ).astimezone(timezone.utc) <= field.constraints.end_date.astimezone(
            timezone.utc,
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


@dataclass
class DistributionTestCase:
    input: ExcelFieldFaker
    expected_distribution: Callable[..., float]


numeric_distributions_sample = [
    DistributionTestCase(
        input=ExcelFieldFaker.parse_field(
            field_name="IntegerField",
            field_type="int",
            constraints={"min_value": 0, "max_value": 100, "distribution": "uniform"},
        ),
        expected_distribution=random.uniform,
    ),
    DistributionTestCase(
        input=ExcelFieldFaker.parse_field(
            field_name="IntegerField",
            field_type="int",
            constraints={
                "mean": 0,
                "standard_deviation": 100,
                "distribution": "normal",
            },
        ),
        expected_distribution=random.normalvariate,
    ),
]


@pytest.mark.parametrize("test_case", numeric_distributions_sample)
def test_numeric_distributions(test_case: DistributionTestCase) -> None:
    assert isinstance(test_case.input.constraints, NumericConstraint)
    assert test_case.input.constraints.distribution == test_case.expected_distribution


def test_numeric_distributions_invalid() -> None:
    distribution = "invalid"

    with pytest.raises(ValueError, match=f"Invalid distribution: {distribution}"):
        ExcelFieldFaker.parse_field(
            field_name="IntegerField",
            field_type="int",
            constraints={
                "min_value": 0,
                "max_value": 100,
                "distribution": distribution,
            },
        )


def test_choice_distributions() -> None:
    allowed_values = ["A", "B", "C"]
    max_range = 1000

    field_faker = ExcelFieldFaker.parse_field(
        field_name="ChoiceField",
        field_type="choice",
        constraints={
            "allowed_values": allowed_values,
            "probabilities": [0, 0.01, 0.99],
        },
    )

    random_sample = [field_faker.get_value() for _ in range(max_range)]

    assert random_sample.count("A") == 0
    assert random_sample.count("B") >= 0
    assert random_sample.count("B") <= max_range // 2
    assert random_sample.count("C") >= max_range // 2
    assert random_sample.count("C") <= max_range


def test_boolean_distributions() -> None:
    max_range = 100

    field_faker = ExcelFieldFaker.parse_field(
        field_name="BooleanField",
        field_type="bool",
        constraints={"probability": 0},
    )
    random_sample = [field_faker.get_value() for _ in range(max_range)]
    assert random_sample.count(str(True)) == 0
    assert random_sample.count(str(False)) == max_range

    field_faker = ExcelFieldFaker.parse_field(
        field_name="BooleanField",
        field_type="bool",
        constraints={"probability": 1},
    )
    random_sample = [field_faker.get_value() for _ in range(max_range)]
    assert random_sample.count(str(True)) == max_range
    assert random_sample.count(str(False)) == 0

    field_faker = ExcelFieldFaker.parse_field(
        field_name="BooleanField",
        field_type="bool",
        constraints={"probability": 0.5},
    )
    random_sample = [field_faker.get_value() for _ in range(max_range)]
    assert random_sample.count(str(True)) >= 0
    assert random_sample.count(str(True)) <= max_range
    assert random_sample.count(str(False)) >= 0
    assert random_sample.count(str(False)) <= max_range
