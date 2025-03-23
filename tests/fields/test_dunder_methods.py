from fexcel.fields import ExcelFieldFaker


def test_field_faker__eq__() -> None:
    faker = ExcelFieldFaker.parse_field("Test", "INTEGER")

    assert faker == ExcelFieldFaker.parse_field("Test", "INTEGER")
    assert faker is not ExcelFieldFaker.parse_field("Test", "INTEGER")
    assert faker != ExcelFieldFaker.parse_field("Test", "TEXT")
    assert faker != "Not an ExcelFieldFaker instance"
