# flake8: noqa: E501, DTZ007

import random
from dataclasses import dataclass
from typing import Callable

import pytest

from fexcel.fields import (
    FexcelField,
)
from fexcel.fields.numeric import FloatFieldFaker

# fmt: off
numeric_field_sample = [
    FexcelField.parse_field("IntegerField", "int"),
    FexcelField.parse_field("IntegerField", "int", min_value=0),
    FexcelField.parse_field("IntegerField", "int", max_value=100),
    FexcelField.parse_field("IntegerField", "int", min_value=0, max_value=100),
    FexcelField.parse_field("FloatingPointField", "float"),
    FexcelField.parse_field("FloatingPointField", "float", min_value=0),
    FexcelField.parse_field("FloatingPointField", "float", max_value=100.0),
    FexcelField.parse_field("FloatingPointField", "float", min_value= 0, max_value=100),
]
# fmt: on


@pytest.mark.parametrize("field", numeric_field_sample)
def test_numeric_constraint(field: FexcelField) -> None:
    assert isinstance(field, FloatFieldFaker)
    assert float(field.get_value()) >= field.min_value
    assert float(field.get_value()) <= field.max_value


def test_invalid_numeric_constraint() -> None:
    with pytest.raises(ValueError, match=r"Invalid 'min_value'"):
        FexcelField.parse_field("IntegerField", "int", min_value="FAIL")


@dataclass
class DistributionTestCase:
    input: FexcelField
    expected_distribution: Callable[..., float]


numeric_distributions_sample = [
    DistributionTestCase(
        input=FexcelField.parse_field(
            field_name="IntegerField",
            field_type="int",
            min_value=0,
            max_value=100,
            distribution="uniform",
        ),
        expected_distribution=random.uniform,
    ),
    DistributionTestCase(
        input=FexcelField.parse_field(
            field_name="IntegerField",
            field_type="int",
            mean=0,
            std=1,
            distribution="normal",
        ),
        expected_distribution=random.normalvariate,
    ),
    DistributionTestCase(
        input=FexcelField.parse_field(
            field_name="FloatField",
            field_type="float",
            mean=0,
            std=1,
            distribution="gaussian",
        ),
        expected_distribution=random.gauss,
    ),
    DistributionTestCase(
        input=FexcelField.parse_field(
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
        FexcelField.parse_field(
            field_name="IntegerField",
            field_type="int",
            **test_case.constraints,
        )
