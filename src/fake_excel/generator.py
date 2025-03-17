import json
from itertools import repeat
from pathlib import Path
from typing import Any, Iterator, Self

from fake_excel.constraint import FieldConstraint, NumericConstraint, TemporalConstraint
from fake_excel.fields import ExcelFieldFaker


class ExcelFaker:
    def __init__(self, schema: list[dict[str, str]]) -> None:
        self._schema = schema
        self._fields = self._parse_fields()

    @classmethod
    def from_file(cls, file: str | Path) -> Self:
        file = Path(file)
        with file.open("r") as fp:
            schema = json.load(fp)
        return cls(schema)

    @property
    def fields(self) -> list[ExcelFieldFaker]:
        return self._fields

    def _parse_fields(self) -> list[ExcelFieldFaker]:
        return [self._parse_field(field) for field in self._schema]

    def _parse_field(self, field: dict[str, Any]) -> ExcelFieldFaker:
        try:
            field_name = field["name"]
            field_type = field["type"]
            constraints = self._parse_constraints(
                field.get("constraints", {}),
                field_type,
            )
            return ExcelFieldFaker(
                field_name,
                field_type,
                constraints,
            )
        except KeyError as err:
            msg = f"Unprocessable field {field}"
            raise ValueError(msg) from err

    def get_fake_records(self, n: int | None = None) -> Iterator[dict[str, str]]:
        generator = repeat(None, n) if n is not None else repeat(None)

        for _ in generator:
            yield {field.name: field.get_value() for field in self._fields}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExcelFaker):
            return False
        return self.fields == other.fields

    def _parse_constraints(
        self,
        constraint: dict[str, Any],
        field_type: str,
    ) -> FieldConstraint:
        if field_type.lower() in ["int", "float", "integer"]:
            return NumericConstraint(**constraint)
        if field_type.lower() in ["date", "datetime"]:
            return TemporalConstraint(**constraint)
        return FieldConstraint(**constraint)

    def __str__(self) -> str:
        ret = "ExcelFaker(\n"
        for field in self.fields:
            ret += f"\t{field}\n"
        ret += ")"
        return ret
