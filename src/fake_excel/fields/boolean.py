from faker import Faker

from fake_excel.constraint import BooleanConstraint, FieldConstraint
from fake_excel.fields.base import ExcelFieldFaker

fake = Faker()


class BooleanFieldFaker(ExcelFieldFaker, faker_types=["bool", "boolean"]):
    constraints: BooleanConstraint

    def get_value(self) -> str:
        return str(fake.boolean(int(self.constraints.probability * 100)))

    def parse_constraints(
        self,
        constraints: dict | None = None,
    ) -> FieldConstraint | None:
        if not isinstance(constraints, dict):
            return BooleanConstraint()
        return BooleanConstraint(probability=constraints.get("probability", 0.5))
