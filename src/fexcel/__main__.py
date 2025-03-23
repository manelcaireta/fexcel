import sys
from argparse import ArgumentParser

from pydantic import BaseModel, ConfigDict

from fexcel.generator import Fexcel


class Args(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    schema_path: str
    output_path: str
    num_fakes: int


def main() -> None:
    args = parse_args()
    fexcel = Fexcel.from_file(args.schema_path)
    fexcel.write_to_file(args.output_path, args.num_fakes)


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

    return Args.model_validate(parser.parse_args(args))


if __name__ == "__main__":
    main()
