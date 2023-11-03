import argparse
from .tokenizer import Tokenizer


def create_parser():
    parser = argparse.ArgumentParser(description='INI parser')
    parser.add_argument('command', type=str, help='available commands: validate, get')
    parser.add_argument('path', type=str, help='path to the INI file to be parsed')
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
    if args.command == 'validate':
        if is_valid:
            print('OK')
        else:
            print("Syntax error in INI file")
    elif args.command == 'get':
        pass
    else:
        print("Wrong command")
        pass


if __name__ == "__main__":
    main()
