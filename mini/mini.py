import argparse
from .tokenizer import Tokenizer


def create_parser():
    parser = argparse.ArgumentParser(description='INI parser')
    group = parser.add_mutually_exclusive_group(required=True)
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
        is_valid = True
    except ValueError as _:
        is_valid = False

    if not is_valid:
        print("Syntax error in INI file")
        return

    if args.validate:
        print('OK')
        return

    if args.json:
        print(doc.to_json())
        return

    if args.get:
        prmkey = args.get
        if args.section:
            print(doc[args.section][prmkey])
        else:
            print(doc[prmkey])


if __name__ == "__main__":
    main()
