import argparse


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference."
    )
    parser.add_argument(
        "-f",
        "--format",
        help="set format of output",
        choices=["nested", "plain", "json"],
        default="nested",
    )
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    return parser
