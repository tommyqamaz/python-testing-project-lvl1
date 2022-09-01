import argparse
import os


def get_parser() -> argparse.ArgumentParser:
    """get parser

    Returns:
        argparse.ArgumentParser: parser
    """
    parser = argparse.ArgumentParser(
        description="Downloades given page and saves it in html format."
    )
    parser.add_argument(
        "-o",
        "--output",
        help="set directory to save",
        default=os.getcwd(),
    )
    parser.add_argument("path")
    return parser
