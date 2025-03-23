import re

import pytest

from fexcel.fields import FexcelField
from tests.fields.test_factory_test_table import FactoryTestCase, test_cases


# NOTE: As this test is fairly fast, we apply it 5 times to catch possible pattern
# pattern errors that pass the first time.
@pytest.mark.parametrize("tt", test_cases * 5)
def test_field_faker_factory(tt: FactoryTestCase) -> None:
    field_faker = FexcelField.parse_field(
        tt.input.name,
        tt.input.type,
    )
    assert isinstance(field_faker, tt.output.type)

    actual = field_faker.get_value()
    expected = re.compile(tt.output.pattern)
    assert re.match(expected, actual) is not None


def test_field_faker_factory_invalid_type() -> None:
    invalid_type = "INVALID_TYPE"

    with pytest.raises(ValueError, match=f"Unknown field type: {invalid_type.lower()}"):
        FexcelField.parse_field("Test", invalid_type)
