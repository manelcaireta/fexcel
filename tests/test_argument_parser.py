import pytest

from fake_excel.__main__ import Args, parse_args


def test_parse_valid_arguments() -> None:
    schema_path = "schema.json"
    output_path = "output.xlsx"
    num_fakes = 10

    args = parse_args([schema_path, output_path, "-n", str(num_fakes)])

    assert isinstance(args, Args)
    assert args.schema_path == schema_path
    assert args.output_path == output_path
    assert args.num_fakes == num_fakes


def test_parse_invalid_arguments() -> None:
    with pytest.raises(SystemExit):
        parse_args([])
