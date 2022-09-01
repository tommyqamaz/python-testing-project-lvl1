import pytest
from page_loader import get_parser
from argparse import Namespace
import os


def test_parser():
    parser = get_parser()

    with pytest.raises(SystemExit) as se:
        parser.parse_args(["-h"])

    assert se.value.code == 0
    assert parser.parse_args(["path"]) == Namespace(output=os.getcwd(), path="path")
