import json
from collections.abc import Iterator
from pathlib import Path

from fake_excel.generator import ExcelFaker


def test_create_fake_excel(schemas_path: Path) -> None:
    with (schemas_path / "test.json").open("r") as f:
        json_schema = json.load(f)

    excel_faker = ExcelFaker(json_schema.get("schema"))
    iterator = excel_faker.get_fake_records()

    assert isinstance(iterator, Iterator)
    record = next(iterator)

    assert isinstance(record, dict)
    assert all(
        isinstance(key, str) and isinstance(value, str) for key, value in record.items()
    )
