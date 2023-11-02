import argparse
from .tokenizer import Tokenizer


def main():
    parser = argparse.ArgumentParser(description='INI parser')
    parser.add_argument('path', type=str, help='path to the INI file to be parsed')
    args = parser.parse_args()
    path = args.path
    with open(path, 'r', encoding="utf-8") as f:
        tokenizer = Tokenizer()
        tokenizer.tokenize_stream(f)
    doc = tokenizer.construct_document()
    print(doc.to_str())


if __name__ == "__main__":
    main()
