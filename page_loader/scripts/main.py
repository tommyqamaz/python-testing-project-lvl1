from page_loader import download
from page_loader import get_parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    download(url_path=args.path, dir=args.output)


if __name__ == "__main__":
    main()
