import sys
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass

from fexcel.generator import Fexcel


@dataclass
class Args:
    schema_path: str
    output_path: str
    num_fakes: int

    @classmethod
    def from_namespace(cls, namespace: Namespace) -> "Args":
        return cls(
            schema_path=namespace.schema_path,
            output_path=namespace.output_path,
            num_fakes=namespace.num_fakes,
        )


def main() -> None:
    try:
        args = parse_args()
        fexcel = Fexcel.from_file(args.schema_path)
        fexcel.write_to_file(args.output_path, args.num_fakes)
    except Exception as e:  # noqa: BLE001
        print(f"fexcel: {e}")
        sys.exit(1)


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

    return Args.from_namespace(parser.parse_args(args))


if __name__ == "__main__":
    main()
