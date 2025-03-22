from faker import Faker

from fake_excel.constraint import FieldConstraint, NumericConstraint
from fake_excel.fields.base import ExcelFieldFaker

fake = Faker()


class IntegerFieldFaker(ExcelFieldFaker, faker_types=["int", "integer"]):
    constraints: NumericConstraint

    def get_value(self) -> str:
        return str(int(self.constraints.rng()))

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        if not isinstance(constraints, dict):
            return NumericConstraint()
        return NumericConstraint(
            distribution=constraints.get("distribution"),
            min_value=constraints.get("min_value"),
            max_value=constraints.get("max_value"),
            mean=constraints.get("mean"),
            std=constraints.get("std"),
        )


class FloatFieldFaker(ExcelFieldFaker, faker_types=["float", "double"]):
    constraints: NumericConstraint

    def get_value(self) -> str:
        return str(self.constraints.rng())

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        if not isinstance(constraints, dict):
            return NumericConstraint()
        return NumericConstraint(
            distribution=constraints.get("distribution"),
            min_value=constraints.get("min_value"),
            max_value=constraints.get("max_value"),
            mean=constraints.get("mean"),
            std=constraints.get("std"),
        )
