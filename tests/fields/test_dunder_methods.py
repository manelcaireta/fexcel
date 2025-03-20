from fake_excel.fields import ExcelFieldFaker


def test_field_faker__eq__() -> None:
    faker = ExcelFieldFaker.parse_field("Test", "INTEGER")

    assert faker == ExcelFieldFaker.parse_field("Test", "INTEGER")
    assert faker is not ExcelFieldFaker.parse_field("Test", "INTEGER")
    assert faker != ExcelFieldFaker.parse_field("Test", "TEXT")
    assert faker != "Not a FieldFaker instance"
