import re
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
    """
    This class represents a lexer and parser for INI configuration files. It can be used to
    construct an IniDocument object from text.
    """

    def __init__(self):
        self.tokens = []

    def tokenize_stream(self, stream):
        """
        Initialize the tokenizer with a stream of INI configuration records.

        For the purpose of this function, a stream is any object that supports iterating over it,
        where each element is thought to represent an INI record.

        For example, if `stream` is a file object returned by `open()`, then each line of the
        file is a separate INI record. Multi-line records are not supported.
        """

        for line in stream:
            rtok = line.strip("\n")
            # Allow any section name that consists solely of letters
            if re.match(r"^\[[a-zA-Z]+\]$", rtok):
                self.tokens.append(Token(TokenKind.SECTION, rtok))
            elif rtok.startswith(";") or rtok.startswith("#"):
                self.tokens.append(Token(TokenKind.COMMENT, rtok))
            elif rtok == "":
                self.tokens.append(Token(TokenKind.EMPTY, rtok))
            # Match any x=y pattern, with an arbitrary amount of whitespace around the equals sign
            elif re.match(r"[0-9a-zA-Z]+\s*\=\s*[0-9a-zA-Z]+$", rtok):
                self.tokens.append(Token(TokenKind.PARAMETER, rtok))
            else:
                self.tokens.append(Token(TokenKind.MALFORMED, rtok))

    def construct_document(self) -> IniDocument:
        """
        Construct an IniDocument object from a previously tokenized stream.

        The tokenizer must be initiated with `tokenize_stream()` prior to calling this method.
        """

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
            elif token.kind in (TokenKind.EMPTY, TokenKind.COMMENT):
                # In an alternative universe, we might preserve comments in the document object, but
                # for now we just ignore them.
                pass
            elif token.kind == TokenKind.MALFORMED:
                raise ValueError(f"Syntax error in token: {repr(token.raw_value)}")
            else:
                raise ValueError(f"Unknown token kind: {repr(token.kind)}")
        return doc
