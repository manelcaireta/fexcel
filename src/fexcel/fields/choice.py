import random
from copy import deepcopy

from fexcel.fields.base import ExcelFieldFaker


class ChoiceFieldFaker(ExcelFieldFaker, faker_types="choice"):
    def __init__(
        self,
        field_name: str,
        *,
        allowed_values: list[str] | None = None,
        probabilities: list[float] | None = None,
    ) -> None:
        self.allowed_values = allowed_values or ["NULL"]
        if not probabilities:
            probabilities = [1 / len(self.allowed_values)] * len(self.allowed_values)
        self.probabilities = self._parse_probabilities(probabilities)
        super().__init__(field_name)

    def get_value(self) -> str:
        choice = random.choices(  # noqa: S311
            population=self.allowed_values,
            weights=self.probabilities,
        )
        return choice[0]

    def _parse_probabilities(self, original_probabilities: list[float]) -> list[float]:
        probabilities = deepcopy(original_probabilities)
        if len(probabilities) <= len(self.allowed_values):
            remaining_probability_space = 1 - sum(probabilities)
            remaining_observations = len(probabilities) - len(self.allowed_values)
            probabilities.extend(
                remaining_probability_space / remaining_observations
                for _ in range(remaining_observations)
            )

        if len(probabilities) > len(self.allowed_values):
            msg = (
                f"Probabilities must have the same length as 'allowed_values' "
                f"or less, got length of probabilities is {len(probabilities)} when "
                f"length of 'allowed_values' is {len(self.allowed_values)}"
            )
            raise ValueError(msg)

        if any(p < 0 for p in probabilities):
            msg = f"Probabilities must be positive, got {probabilities}"
            raise ValueError(msg)

        if sum(probabilities) != 1:
            msg = f"Probabilities must sum up to 1, got {sum(probabilities)}"
            raise ValueError(msg)

        return probabilities
