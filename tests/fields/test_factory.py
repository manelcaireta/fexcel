import re

import pytest

from fake_excel.fields import ExcelFieldFaker
from tests.fields.test_factory_test_table import FactoryTestCase, test_cases


@pytest.mark.parametrize("tt", test_cases * 5)
def test_field_faker_factory(tt: FactoryTestCase) -> None:
    field_faker = ExcelFieldFaker.parse_field(
        tt.input.name,
        tt.input.type,
    )
    assert isinstance(field_faker, tt.output.type)

    actual = field_faker.get_value()
    expected = re.compile(tt.output.pattern)
    assert re.match(expected, actual) is not None


def test_field_faker_factory_invalid_type() -> None:
    with pytest.raises(ValueError, match="Unknown field type: INVALID_TYPE"):
        ExcelFieldFaker.parse_field("Test", "INVALID_TYPE")
