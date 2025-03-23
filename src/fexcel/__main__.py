import sys
from argparse import ArgumentParser

from pydantic import BaseModel, ConfigDict
from pyexcel import isave_as

from fexcel.generator import ExcelFaker


class Args(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    schema_path: str
    output_path: str
    num_fakes: int


def main() -> None:
    args = parse_args()
    fake = ExcelFaker.from_file(args.schema_path)
    iterator = fake.get_fake_records(args.num_fakes)
    isave_as(records=iterator, dest_file_name=args.output_path, sheet_name="Sheet 1")


def parse_args(args: list[str] = sys.argv[1:]) -> Args:
    parser = ArgumentParser()
    parser.add_argument("schema_path", type=str, help="Path to the schema file")
    parser.add_argument("output_path", type=str, help="Path to the output file")
    parser.add_argument(
        "-n",
        "--num-fakes",
        type=int,
        default=1000,
        help="Number of fake records to generate",
    )

    try:
        return Args.model_validate(parser.parse_args(args))
    except SystemExit:
        print()
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
