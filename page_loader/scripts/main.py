from page_loader import download
from page_loader import get_parser
import sys


def main():
    parser = get_parser()
    args = parser.parse_args()
    result = download(url=args.path, dir=args.output)
    if result:
        print(f"Page was downloaded as '{result}'")
    else:
        exit(1)


if __name__ == "__main__":
    main()
