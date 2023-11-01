from enum import Enum
from mini.document import IniDocument

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
                ## TODO: ooops
                pass
            else:
                raise ValueError(f"Unknown token kind: {token.kind}")
        return doc