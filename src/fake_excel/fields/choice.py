import random

from fake_excel.constraint import ChoiceConstraint, FieldConstraint
from fake_excel.fields.base import ExcelFieldFaker


class ChoiceFieldFaker(ExcelFieldFaker, faker_types="choice"):
    constraints: ChoiceConstraint

    def get_value(self) -> str:
        choice = random.choices(  # noqa: S311
            population=self.constraints.allowed_values,
            weights=self.constraints.probabilities,
        )
        return choice[0]

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        if not isinstance(constraints, dict):
            return ChoiceConstraint()
        return ChoiceConstraint(
            allowed_values=constraints.get("allowed_values"),
            probabilities=constraints.get("probabilities"),
        )
