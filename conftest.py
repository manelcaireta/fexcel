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
