import json
from collections.abc import Callable
from pathlib import Path
from typing import Iterator, Self

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
    "float": lambda: fake.random_number() / (fake.random_number() or 10),
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

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, ExcelFieldFaker):
            return False
        return self.name == value.name and self._type == value._type


class ExcelFaker:
    def __init__(self, schema: list[dict[str, str]]) -> None:
        self._schema = schema
        self._fields = self._parse_fields()

    @classmethod
    def from_file(cls, file: str | Path) -> Self:
        file = Path(file)
        with file.open("r") as fp:
            schema = json.load(fp)
        return cls(schema["schema"])

    @property
    def fields(self) -> list[ExcelFieldFaker]:
        return self._fields

    def _parse_fields(self) -> list[ExcelFieldFaker]:
        return [self._parse_field(field) for field in self._schema]

    def _parse_field(self, field: dict[str, str]) -> ExcelFieldFaker:
        try:
            field_name = field["name"]
            field_type = field["type"]
            return ExcelFieldFaker(field_name, field_type)
        except KeyError as err:
            raise ValueError(f"Unprocessable field {field}") from err

    def get_fake_records(self) -> Iterator[dict[str, str]]:
        while True:
            yield {field.name: field.get_value() for field in self._fields}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExcelFaker):
            return False
        return self.fields == other.fields
