import json
from collections.abc import Iterator
from datetime import datetime, timedelta
from pathlib import Path

from faker import Faker
from pyexcel import isave_as

MAX_FAKES = 1000

MIN_YEAR = 2024

fake = Faker()


def main() -> None:
    excel_schema = parse_json("test.json")["schema"]
    validate_json(excel_schema)

    isave_as(
        records=list(fake_values(excel_schema)),
        dest_file_name="test.xlsx",
        sheet_name="Sheet1",
        column_names=list(excel_schema.keys()),
    )


def parse_json(path: str) -> dict:
    with Path(path).open("r") as fp:
        return json.load(fp)


def validate_json(json_data: dict[str, str]) -> None:
    if not isinstance(json_data, dict):
        raise ValueError("JSON data must be a dictionary")

    for key, value in json_data.items():
        if not isinstance(key, str):
            raise ValueError("All keys must be strings")
        if not isinstance(value, str):
            raise ValueError("All values must be strings")


def fake_values(schema: dict[str, str]) -> Iterator[dict[str, str]]:
    for _ in range(MAX_FAKES):
        record = {}
        for key, value in schema.items():
            lower_value = value.lower()
            if lower_value.startswith("type:"):
                list_of_types = value.lstrip("type:").split(",")
                record[key] = fake.random_element(list_of_types)
            elif lower_value == "name":
                record[key] = fake.name()
            elif lower_value == "email":
                record[key] = fake.email()
            elif lower_value == "phone":
                record[key] = fake.phone_number()
            elif lower_value == "address":
                record[key] = fake.address()
            elif lower_value == "date":
                record[key] = fake.date()
            elif lower_value == "time":
                record[key] = fake.time()
            elif lower_value == "datetime":
                record[key] = (
                    (
                        datetime(year=MIN_YEAR, month=1, day=1)
                        + fake.time_delta(datetime.now() + timedelta(days=365))
                    )
                    #.replace(microsecond=0)
                    .isoformat()
                )
            elif lower_value.startswith("datetime>"):
                name = lower_value.split(">")[1].strip()
                record[key] = (
                    (datetime.fromisoformat(record[name]) + fake.time_delta())
                    #.replace(microsecond=0)
                    .isoformat()
                )
            elif lower_value == "text":
                record[key] = fake.text()
            elif lower_value == "integer":
                record[key] = str(fake.random_int())
            elif lower_value == "float":
                record[key] = str(fake.random_number())
            elif lower_value == "boolean":
                record[key] = str(fake.boolean())
            elif lower_value == "url":
                record[key] = fake.url()
            elif lower_value == "ipv4":
                record[key] = fake.ipv4()
            elif lower_value == "ipv6":
                record[key] = fake.ipv6()
            elif lower_value == "uuid":
                record[key] = str(fake.uuid4())
            elif lower_value == "location":
                record[key] = fake.locale()
        yield record


if __name__ == "__main__":
    main()
