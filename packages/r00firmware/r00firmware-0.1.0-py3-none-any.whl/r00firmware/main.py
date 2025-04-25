# r00firmware/main.py
import sys
from .cli import create_parser

def main():
    parser = create_parser()
    try:
        args = parser.parse_args()
    except SystemExit as e:
        sys.exit(e.code)

    try:
        args.func(args)
    except Exception as e:
        print(f"Произошла ошибка при выполнении команды: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()