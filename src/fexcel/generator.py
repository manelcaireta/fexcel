import json
from itertools import repeat
from pathlib import Path
from typing import Any, Iterator, Self

import pyexcel as pe

from fexcel.fields import FexcelField


class Fexcel:
    """
    Fexcel is the main class of the `fexcel` package, designed to generate fake excel
    files based on a provided schema. It provides methods to parse schema definitions,
    generate fake records, and write them to an Excel file.

    It can be instantiated either as any normal class passing the schema as a python
    dictionary or through its method `from_file` to read a JSON file containing the
    schema.
    """

    def __init__(self, schema: list[dict[str, str]]) -> None:
        self._schema = schema
        self._fields = self._parse_fields()

    @classmethod
    def from_file(cls, file: str | Path) -> Self:
        """
        Create an instance of Fexcel from a JSON schema file.

        :param file: Path to the JSON schema file.
        :type file: str | Path
        :return: An instance of the Fexcel class.
        :rtype: Self
        """
        file = Path(file)
        with file.open("r") as fp:
            schema = json.load(fp)
        return cls(schema)

    @property
    def fields(self) -> list[FexcelField]:
        """
        Get the list of parsed fields.

        :return: A list of FexcelField objects.
        :rtype: list[:class:`FexcelField`]
        """
        return self._fields

    def _parse_fields(self) -> list[FexcelField]:
        return [self._parse_field(field) for field in self._schema]

    def _parse_field(self, field: dict[str, Any]) -> FexcelField:
        try:
            constraints = field.get("constraints", {})
            return FexcelField.parse_field(
                field_name=field["name"],
                field_type=field["type"],
                **constraints,
            )
        except ValueError as err:
            msg = f"Error parsing field '{field['name']}': {err}"
            raise ValueError(msg) from err
        except KeyError as err:
            msg = f"Error parsing field '{field}': {err} key not found"
            raise ValueError(msg) from err

    def get_fake_records(self, n: int | None = None) -> Iterator[dict[str, str]]:
        """
        Generate an iterator of fake records based on the schema.

        :param n: The number of fake records to generate. If None, generates an infinite
        number of records.
        :type n: int | None, optional
        :return: An iterator yielding dictionaries representing fake records.
        :rtype: Iterator[dict[str, str]]
        """
        generator = repeat(None, n) if n is not None else repeat(None)

        for _ in generator:
            yield {field.name: field.get_value() for field in self._fields}

    def write_to_file(
        self,
        file_path: str | Path,
        num_fakes: int = 1000,
        sheet_name: str = "Sheet1",
    ) -> None:
        """
        Generate and write fake records based on the schema in an excel file.

        :param file_path: Path to the file where the excel data will be written.
        :type file_path: str | Path
        :param num_fakes: Number of fake records to create, defaults to 1000
        :type num_fakes: int, optional
        :param sheet_name: Name for the excel sheet to be created, defaults to "Sheet1"
        :type sheet_name: str, optional
        """

        file_path = Path(file_path).resolve()
        iterator = self.get_fake_records(num_fakes)
        pe.isave_as(
            records=iterator,
            dest_file_name=str(file_path),
            sheet_name=sheet_name,
        )
        sheet = pe.get_sheet(
            file_name=str(file_path),
            name_columns_by_row=0,
        )
        sheet = sheet.project([field.name for field in self.fields])
        sheet.save_as(str(file_path))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Fexcel):
            return False
        return self.fields == other.fields

    def __str__(self) -> str:
        ret = "ExcelFaker(\n"
        for field in self.fields:
            ret += f"\t{field}\n"
        ret += ")"
        return ret
