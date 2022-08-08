import argparse


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Downloades given page and saves it in html format."
    )
    parser.add_argument(
        "-o",
        "--output",
        help="set directory to save",
        default="cwd",
    )
    parser.add_argument("path")
    return parser
