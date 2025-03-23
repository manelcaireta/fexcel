from fexcel.fields import FexcelField


def test_field_faker__eq__() -> None:
    faker = FexcelField.parse_field("Test", "INTEGER")

    assert faker == FexcelField.parse_field("Test", "INTEGER")
    assert faker is not FexcelField.parse_field("Test", "INTEGER")
    assert faker != FexcelField.parse_field("Test", "TEXT")
    assert faker != "Not an ExcelFieldFaker instance"
