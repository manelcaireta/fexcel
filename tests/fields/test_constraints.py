# flake8: noqa: E501, DTZ007

import random
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

import pytest

from fexcel.fields import (
    DateFieldFaker,
    DateTimeFieldFaker,
    ExcelFieldFaker,
)
from fexcel.fields.numeric import FloatFieldFaker

# SIMPLE CONSTRAINT TESTS

# fmt: off
numeric_field_sample = [
    ExcelFieldFaker.parse_field("IntegerField", "int"),
    ExcelFieldFaker.parse_field("IntegerField", "int", min_value=0),
    ExcelFieldFaker.parse_field("IntegerField", "int", max_value=100),
    ExcelFieldFaker.parse_field("IntegerField", "int", min_value=0, max_value=100),
    ExcelFieldFaker.parse_field("FloatingPointField", "float"),
    ExcelFieldFaker.parse_field("FloatingPointField", "float", min_value=0),
    ExcelFieldFaker.parse_field("FloatingPointField", "float", max_value=100.0),
    ExcelFieldFaker.parse_field("FloatingPointField", "float", min_value= 0, max_value=100),
]
# fmt: on


@pytest.mark.parametrize("field", numeric_field_sample)
def test_numeric_constraint(field: ExcelFieldFaker) -> None:
    assert isinstance(field, FloatFieldFaker)
    assert float(field.get_value()) >= field.min_value
    assert float(field.get_value()) <= field.max_value


# fmt: off
temporal_field_sample = [
    ExcelFieldFaker.parse_field("DateField", "date"),
    ExcelFieldFaker.parse_field("DateField", "date", start_date="2023-01-01"),
    ExcelFieldFaker.parse_field("DateField", "date", end_date="2023-12-31"),
    ExcelFieldFaker.parse_field("DateField", "date", start_date="2023-01-01", end_date="2023-12-31"),
    ExcelFieldFaker.parse_field("DateTimeField", "datetime"),
    ExcelFieldFaker.parse_field("DateTimeField", "datetime", start_date="2023-01-01"),
    ExcelFieldFaker.parse_field("DateTimeField", "datetime", end_date="2023-12-31"),
    ExcelFieldFaker.parse_field("DateTimeField", "datetime", start_date="2023-01-01", end_date="2023-12-31"),
]
# fmt: on


@pytest.mark.parametrize("field", temporal_field_sample)
def test_temporal_constraint(field: ExcelFieldFaker) -> None:
    assert isinstance(field, DateFieldFaker | DateTimeFieldFaker)

    if field.start_date is not None:
        got = datetime.strptime(field.get_value(), field.format_string)
        assert got.astimezone(timezone.utc) >= field.start_date.astimezone(timezone.utc)
    if field.end_date is not None:
        got = datetime.strptime(field.get_value(), field.format_string)
        assert got.astimezone(timezone.utc) <= field.end_date.astimezone(timezone.utc)


def test_choice_constraint() -> None:
    allowed_values = ["A", "B", "C"]

    field_faker = ExcelFieldFaker.parse_field(
        field_name="ChoiceField",
        field_type="choice",
        allowed_values=allowed_values,
    )

    for _ in range(100):
        assert field_faker.get_value() in allowed_values


# DISTRIBUTION TESTS


@dataclass
class DistributionTestCase:
    input: ExcelFieldFaker
    expected_distribution: Callable[..., float]


numeric_distributions_sample = [
    DistributionTestCase(
        input=ExcelFieldFaker.parse_field(
            field_name="IntegerField",
            field_type="int",
            min_value=0,
            max_value=100,
            distribution="uniform",
        ),
        expected_distribution=random.uniform,
    ),
    DistributionTestCase(
        input=ExcelFieldFaker.parse_field(
            field_name="IntegerField",
            field_type="int",
            mean=0,
            std=1,
            distribution="normal",
        ),
        expected_distribution=random.normalvariate,
    ),
    DistributionTestCase(
        input=ExcelFieldFaker.parse_field(
            field_name="FloatField",
            field_type="float",
            mean=0,
            std=1,
            distribution="gaussian",
        ),
        expected_distribution=random.gauss,
    ),
    DistributionTestCase(
        input=ExcelFieldFaker.parse_field(
            field_name="FloatField",
            field_type="float",
            mean=0,
            std=1,
            distribution="lognormal",
        ),
        expected_distribution=random.lognormvariate,
    ),
]


@pytest.mark.parametrize("test_case", numeric_distributions_sample)
def test_numeric_distributions(test_case: DistributionTestCase) -> None:
    assert isinstance(test_case.input, FloatFieldFaker)
    assert test_case.input.rng.func == test_case.expected_distribution


@dataclass
class InvalidDistributionTestCase:
    constraints: dict
    expected_exception_match: str


invalid_numeric_distributions_sample = [
    InvalidDistributionTestCase(
        constraints={
            "min_value": 0,
            "max_value": 100,
            "distribution": "invalid",
        },
        expected_exception_match=r"Invalid distribution.*?",
    ),
    InvalidDistributionTestCase(
        constraints={
            "mean": 0,
            "std": 1,
            "min_value": 0,
            "max_value": 100,
            "distribution": "normal",
        },
        expected_exception_match=r"Cannot specify both min_value/max_value and mean/std",
    ),
    InvalidDistributionTestCase(
        constraints={
            "min_value": 0,
            "max_value": 1,
            "distribution": "gaussian",
        },
        expected_exception_match=r"Cannot specify min_value/max_value with gaussian distribution",
    ),
    InvalidDistributionTestCase(
        constraints={
            "mean": 0,
            "std": 1,
            "distribution": "uniform",
        },
        expected_exception_match=r"Cannot specify mean/std with uniform distribution",
    ),
    InvalidDistributionTestCase(
        constraints={
            "min_value": 1,
            "max_value": 0,
            "distribution": "uniform",
        },
        expected_exception_match=r"min_value must be less than or equal than max_value",
    ),
]


@pytest.mark.parametrize("test_case", invalid_numeric_distributions_sample)
def test_numeric_distributions_invalid(test_case: InvalidDistributionTestCase) -> None:
    with pytest.raises(ValueError, match=test_case.expected_exception_match):
        ExcelFieldFaker.parse_field(
            field_name="IntegerField",
            field_type="int",
            **test_case.constraints,
        )


def test_choice_distributions() -> None:
    allowed_values = ["A", "B", "C"]
    max_range = 1000

    field_faker = ExcelFieldFaker.parse_field(
        field_name="ChoiceField",
        field_type="choice",
        allowed_values=allowed_values,
        probabilities=[0, 0.01, 0.99],
    )

    random_sample = [field_faker.get_value() for _ in range(max_range)]

    assert random_sample.count("A") == 0
    assert random_sample.count("B") >= 0
    assert random_sample.count("B") <= max_range // 2
    assert random_sample.count("C") >= max_range // 2
    assert random_sample.count("C") <= max_range


def test_invalid_choice_distribution() -> None:
    allowed_values = ["A", "B", "C"]

    probabilities = [0.5, 0.5, 0.5]
    with pytest.raises(ValueError, match=r"Probabilities must sum up to 1, got .*"):
        ExcelFieldFaker.parse_field(
            field_name="ChoiceField",
            field_type="choice",
            allowed_values=allowed_values,
            probabilities=probabilities,
        )

    probabilities = [-1]
    with pytest.raises(ValueError, match=r"Probabilities must be positive, got .*"):
        ExcelFieldFaker.parse_field(
            field_name="ChoiceField",
            field_type="choice",
            allowed_values=allowed_values,
            probabilities=probabilities,
        )
    probabilities = [0.1] * (len(allowed_values) + 1)
    with pytest.raises(
        ValueError,
        match=r"Probabilities must have the same length as 'allowed_values' or less.*",
    ):
        ExcelFieldFaker.parse_field(
            field_name="ChoiceField",
            field_type="choice",
            allowed_values=allowed_values,
            probabilities=probabilities,
        )


def test_boolean_distributions() -> None:
    max_range = 100

    field_faker = ExcelFieldFaker.parse_field(
        field_name="BooleanField",
        field_type="bool",
        probability=0,
    )
    random_sample = [field_faker.get_value() for _ in range(max_range)]
    assert random_sample.count(str(True)) == 0
    assert random_sample.count(str(False)) == max_range

    field_faker = ExcelFieldFaker.parse_field(
        field_name="BooleanField",
        field_type="bool",
        probability=1,
    )
    random_sample = [field_faker.get_value() for _ in range(max_range)]
    assert random_sample.count(str(True)) == max_range
    assert random_sample.count(str(False)) == 0

    field_faker = ExcelFieldFaker.parse_field(
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
        ExcelFieldFaker.parse_field(
            field_name="BooleanField",
            field_type="bool",
            probability=-1,
        )
    with pytest.raises(
        ValueError,
        match=r"Probability must be between 0 and 1, got .*",
    ):
        ExcelFieldFaker.parse_field(
            field_name="BooleanField",
            field_type="bool",
            probability=2,
        )
