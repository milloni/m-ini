from enum import Enum


class TokenKind(Enum):
    SECTION = 1
    PARAMETER = 2
    COMMENT = 3
    EMPTY = 4
    MALFORMED = 5


class Token:
    def __init__(self, kind: TokenKind, raw_value: str):
        self.kind = kind
        self.raw_value = raw_value


class Tokenizer:
    def __init__(self):
        self.tokens = []

    def tokenize_stream(self, stream):
        # For the purpose of this function, a stream is any object that supports iterating over it,
        # where each element is thought to represent an entry in the configuration file.
        for line in stream:
            if line.startswith("[") and line.endswith("]"):
                self.tokens.append(Token(TokenKind.SECTION, line))
            elif line.startswith(";") or line.startswith("#"):
                self.tokens.append(Token(TokenKind.COMMENT, line))
            elif line == "":
                self.tokens.append(Token(TokenKind.EMPTY, line))
            elif "=" in line:
                self.tokens.append(Token(TokenKind.PARAMETER, line))
            else:
                self.tokens.append(Token(TokenKind.MALFORMED, line))

    def tokens(self):
        return self.tokens
