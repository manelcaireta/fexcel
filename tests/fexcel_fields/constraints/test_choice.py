# flake8: noqa: E501, DTZ007


import pytest

from fexcel.fields import (
    FexcelField,
)


def test_choice_constraint() -> None:
    allowed_values = ["A", "B", "C"]

    field_faker = FexcelField.parse_field(
        field_name="ChoiceField",
        field_type="choice",
        allowed_values=allowed_values,
    )

    for _ in range(100):
        assert field_faker.get_value() in allowed_values


def test_choice_distributions() -> None:
    allowed_values = ["A", "B", "C"]
    max_range = 1000

    field_faker = FexcelField.parse_field(
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
        FexcelField.parse_field(
            field_name="ChoiceField",
            field_type="choice",
            allowed_values=allowed_values,
            probabilities=probabilities,
        )

    probabilities = [-1]
    with pytest.raises(ValueError, match=r"Probabilities must be positive, got .*"):
        FexcelField.parse_field(
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
        FexcelField.parse_field(
            field_name="ChoiceField",
            field_type="choice",
            allowed_values=allowed_values,
            probabilities=probabilities,
        )
