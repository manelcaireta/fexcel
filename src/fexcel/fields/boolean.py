from faker import Faker

from fexcel.fields.base import ExcelFieldFaker

fake = Faker()


class BooleanFieldFaker(ExcelFieldFaker, faker_types=["bool", "boolean"]):
    def __init__(
        self,
        field_name: str,
        *,
        probability: float = 0.5,
    ) -> None:
        if probability < 0 or probability > 1:
            msg = f"Probability must be between 0 and 1, got {probability}"
            raise ValueError(msg)
        self.probability = probability
        self.probability = probability
        super().__init__(field_name)

    def get_value(self) -> str:
        return str(fake.boolean(int(self.probability * 100)))
