import argparse
from .tokenizer import Tokenizer


def create_parser():
    parser = argparse.ArgumentParser(description='INI parser')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--validate', action='store_true', help='validate INI file')
    group.add_argument('--get', type=str, help='get value from INI file')
    group.add_argument('--json', action='store_true', help='convert INI file to JSON')
    parser.add_argument('--section', type=str, help='specifiy section (use with --get)')
    parser.add_argument('path', type=str, help='path to INI file to be parsed')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    with open(args.path, 'r', encoding="utf-8") as f:
        tokenizer = Tokenizer()
        tokenizer.tokenize_stream(f)
    try:
        doc = tokenizer.construct_document()
    except ValueError as _:
        print("Syntax error in INI file")
        return

    if args.validate:
        print('OK')
        return

    if args.json:
        print(doc.to_json())
        return

    if args.get:
        propkey = args.get
        if args.section:
            print(doc[args.section][propkey])
        else:
            print(doc[propkey])


if __name__ == "__main__":
    main()
