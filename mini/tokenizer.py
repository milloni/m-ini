from enum import Enum
from dataclasses import dataclass
from .document import IniDocument


class TokenKind(Enum):
    SECTION = 1
    PARAMETER = 2
    COMMENT = 3
    EMPTY = 4
    MALFORMED = 5


@dataclass
class Token:
    kind: TokenKind
    raw_value: str


class Tokenizer:
    def __init__(self):
        self.tokens = []

    def tokenize_stream(self, stream):
        # For the purpose of this function, a stream is any object that supports iterating over it,
        # where each element is thought to represent an entry in the configuration file.
        for line in stream:
            rtok = line.strip("\n")
            if rtok.startswith("[") and rtok.endswith("]"):
                self.tokens.append(Token(TokenKind.SECTION, rtok))
            elif rtok.startswith(";") or rtok.startswith("#"):
                self.tokens.append(Token(TokenKind.COMMENT, rtok))
            elif rtok == "":
                self.tokens.append(Token(TokenKind.EMPTY, rtok))
            elif "=" in rtok:
                self.tokens.append(Token(TokenKind.PARAMETER, rtok))
            else:
                self.tokens.append(Token(TokenKind.MALFORMED, rtok))

    def construct_document(self):
        # Keep track of what section we're in. `None` means the default section.
        current_section = None
        doc = IniDocument()

        for token in self.tokens:
            if token.kind == TokenKind.SECTION:
                current_section = token.raw_value.strip("[]")
                doc.add_section(current_section)
            elif token.kind == TokenKind.PARAMETER:
                key, value = [x.strip() for x in token.raw_value.split("=")]
                if current_section:
                    doc[current_section][key] = value
                else:
                    doc[key] = value
            elif token.kind == TokenKind.EMPTY:
                pass
            elif token.kind == TokenKind.COMMENT:
                # In an alternative universe, we might preserve comments in the document object, but
                # for now we just ignore them.
                pass
            elif token.kind == TokenKind.MALFORMED:
                raise ValueError(f"Syntax error in token: {repr(token.raw_value)}")
            else:
                raise ValueError(f"Unknown token kind: {repr(token.kind)}")
        return doc
