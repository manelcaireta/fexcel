class ExcelFieldFaker:
    def __init__(self, field_name: str, field_type: str) -> None:
        self._name = field_name
        self._type = field_type
        self._record_generator = None


class ExcelFaker:
    def __init__(self, schema: list[dict[str, str]]) -> None:
        self._schema = schema

    def get_fields(self) -> list[ExcelFieldFaker]:
        return [self._parse_field(field) for field in self._schema]

    def _parse_field(self, field: dict[str, str]) -> ExcelFieldFaker:
        try:
            field_name = field["name"]
            field_type = field["type"]
            return ExcelFieldFaker(field_name, field_type)
        except KeyError as err:
            raise ValueError(f"Unprocessable field {field}") from err
