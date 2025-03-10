from collections.abc import Callable

from faker import Faker

from fake_excel.constraint import FieldConstraint

fake = Faker()

type_to_generator = {
    "name": fake.name,
    "email": fake.email,
    "phone": fake.phone_number,
    "address": fake.address,
    "date": fake.date,
    "time": fake.time,
    "datetime": fake.date_time,
    "text": fake.text,
    "int": fake.random_int,
    "integer": fake.random_int,
    "float": lambda: fake.random_number() / (fake.random_number() or 10),
    "boolean": fake.boolean,
    "url": fake.url,
    "ipv4": fake.ipv4,
    "ipv6": fake.ipv6,
    "uuid": fake.uuid4,
    "location": fake.locale,
}


class ExcelFieldFaker:
    def __init__(
        self,
        field_name: str,
        field_type: str,
        field_constraints: FieldConstraint,
    ) -> None:
        self.name = field_name
        self._type = field_type.lower()
        self._value_creator = None
        self._constraints = field_constraints
        self._last_value = None

    def get_value(self) -> str:
        if self._value_creator is None:
            self._value_creator = self._get_value_creator()
        return str(self._value_creator())

    def _get_value_creator(self) -> Callable[[], str]:
        if self._constraints.allowed_values is not None:
            values = self._constraints.allowed_values.copy()
            return lambda: fake.random_element(values)
        return type_to_generator.get(self._type, lambda *_args, **_kwargs: "NULL")

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, ExcelFieldFaker):
            return False
        return self.name == value.name and self._type == value._type
