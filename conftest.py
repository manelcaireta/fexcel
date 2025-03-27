import random
from pathlib import Path

import pytest


@pytest.fixture
def data_path() -> Path:
    data_path = Path(__file__).parent / "tests" / "data"
    data_path.mkdir(exist_ok=True)
    return data_path


@pytest.fixture
def input_path(data_path: Path) -> Path:
    input_path = data_path / "inputs"
    input_path.mkdir(exist_ok=True)
    return input_path


@pytest.fixture
def output_path(data_path: Path) -> Path:
    output_path = data_path / "outputs"
    output_path.mkdir(exist_ok=True)
    return output_path


@pytest.fixture(scope="session")
def random_field_sample() -> list[dict[str, str]]:
    text_fields = [
        {"name": f"Text-{i}", "type": "text"} for i in range(random.randint(1, 100))
    ]
    int_fields = [
        {"name": f"Int-{i}", "type": "int"} for i in range(random.randint(1, 100))
    ]
    bool_fields = [
        {"name": f"Bool-{i}", "type": "bool"} for i in range(random.randint(1, 100))
    ]
    float_fields = [
        {"name": f"Float-{i}", "type": "float"} for i in range(random.randint(1, 100))
    ]
    date_fields = [
        {"name": f"Date-{i}", "type": "date"} for i in range(random.randint(1, 100))
    ]

    return text_fields + int_fields + bool_fields + float_fields + date_fields
