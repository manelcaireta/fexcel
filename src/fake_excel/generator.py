from collections.abc import Callable
from typing import Iterator

from faker import Faker

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
    "integer": fake.random_int,
    "float": fake.random_number,
    "boolean": fake.boolean,
    "url": fake.url,
    "ipv4": fake.ipv4,
    "ipv6": fake.ipv6,
    "uuid": fake.uuid4,
}


class ExcelFieldFaker:
    def __init__(self, field_name: str, field_type: str) -> None:
        self.name = field_name
        self._type = field_type.lower()
        self._value_creator = None

    def get_value(self) -> str:
        if self._value_creator is None:
            self._value_creator = self._get_value_creator()
        return str(self._value_creator())

    def _get_value_creator(self) -> Callable[[], str]:
        return type_to_generator.get(self._type, lambda *_args, **_kwargs: "NULL")


class ExcelFaker:
    def __init__(self, schema: list[dict[str, str]]) -> None:
        self._schema = schema

    def get_fake_records(self) -> Iterator[dict[str, str]]:
        while True:
            yield {field.name: field.get_value() for field in self.get_fields()}

    def get_fields(self) -> list[ExcelFieldFaker]:
        return [self._parse_field(field) for field in self._schema]

    def _parse_field(self, field: dict[str, str]) -> ExcelFieldFaker:
        try:
            field_name = field["name"]
            field_type = field["type"]
            return ExcelFieldFaker(field_name, field_type)
        except KeyError as err:
            raise ValueError(f"Unprocessable field {field}") from err
