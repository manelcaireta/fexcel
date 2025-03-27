from fexcel import FexcelField


def test_valid_text() -> None:
    field = FexcelField.parse_field("TextField", "text")
    for _ in range(100):
        assert "\n" not in field.get_value()
