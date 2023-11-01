import pytest
from mini.tokenizer import Tokenizer, TokenKind


def test_tokenizer_good():
    s = [
        "[data]",
        "name = Leon",
        "",
        "; semicolon indicates a comment",
        "# and so does a hash",
    ]
    tokenizer = Tokenizer()
    tokenizer.tokenize_stream(s)

    # Trade off between test simplicity and performance. If not O(1) access, can be slow
    assert tokenizer.tokens[0].kind == TokenKind.SECTION
    assert tokenizer.tokens[1].kind == TokenKind.PARAMETER
    assert tokenizer.tokens[2].kind == TokenKind.EMPTY
    assert tokenizer.tokens[3].kind == TokenKind.COMMENT
    assert tokenizer.tokens[4].kind == TokenKind.COMMENT


def test_tokenizer_malformed():
    s = [
        "[data]",
        "name = Leon",
        "",
        "; semicolon indicates a comment",
        "# and so does a hash",
        "[code",
    ]
    tokenizer = Tokenizer()
    tokenizer.tokenize_stream(s)

    # Trade off between test simplicity and performance. If not O(1) access, can be slow
    assert tokenizer.tokens[0].kind == TokenKind.SECTION
    assert tokenizer.tokens[1].kind == TokenKind.PARAMETER
    assert tokenizer.tokens[2].kind == TokenKind.EMPTY
    assert tokenizer.tokens[3].kind == TokenKind.COMMENT
    assert tokenizer.tokens[4].kind == TokenKind.COMMENT
    assert tokenizer.tokens[5].kind == TokenKind.MALFORMED