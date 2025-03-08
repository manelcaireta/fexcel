import pathlib

import pytest


@pytest.fixture
def schemas_path() -> pathlib.Path:
    return pathlib.Path(__file__).parent / "tests" / "data" / "schemas"
