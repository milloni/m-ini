import os
import pathlib
import pytest
from mini.tokenizer import Tokenizer, TokenKind

data_path = pathlib.Path(os.path.dirname(__file__)).joinpath("data")


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

    assert tokenizer.tokens[0].kind == TokenKind.SECTION
    assert tokenizer.tokens[1].kind == TokenKind.PARAMETER
    assert tokenizer.tokens[2].kind == TokenKind.EMPTY
    assert tokenizer.tokens[3].kind == TokenKind.COMMENT
    assert tokenizer.tokens[4].kind == TokenKind.COMMENT


def test_document_construction():
    s = [
        "[data]",
        "name = Leon",
        "",
        "; semicolon indicates a comment",
        "# and so does a hash",
    ]
    tokenizer = Tokenizer()
    tokenizer.tokenize_stream(s)

    doc = tokenizer.construct_document()
    assert doc["data"]["name"] == "Leon"


def test_document_construction2():
    ini_path = data_path.joinpath("hello.ini")
    with open(ini_path, 'r', encoding="utf-8") as f:
        tokenizer = Tokenizer()
        tokenizer.tokenize_stream(f)
    doc = tokenizer.construct_document()
    assert doc["language"] == "Polish"
    assert doc["location"] == "Poland"
    assert doc["pet"]["name"] == "Leon"
    assert doc["pet"]["species"] == "cat"


def test_whitespace():
    ini_path = data_path.joinpath("whitespace.ini")
    with open(ini_path, 'r', encoding="utf-8") as f:
        tokenizer = Tokenizer()
        tokenizer.tokenize_stream(f)
    doc = tokenizer.construct_document()
    assert doc["bed"] == "sleeping"
    assert doc["chair"] == "sitting"
    assert doc["road"] == "driving"
    assert doc["floor"] == "standing"
    assert doc["garden"] == "gardening"


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

    assert tokenizer.tokens[0].kind == TokenKind.SECTION
    assert tokenizer.tokens[1].kind == TokenKind.PARAMETER
    assert tokenizer.tokens[2].kind == TokenKind.EMPTY
    assert tokenizer.tokens[3].kind == TokenKind.COMMENT
    assert tokenizer.tokens[4].kind == TokenKind.COMMENT
    assert tokenizer.tokens[5].kind == TokenKind.MALFORMED


def test_construct_document_error():
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
    with pytest.raises(ValueError):
        tokenizer.construct_document()


def test_parse_numbers():
    s = [
        "[data]",
        "age = 20"
    ]
    tokenizer = Tokenizer()
    tokenizer.tokenize_stream(s)
    assert tokenizer.tokens[0].kind == TokenKind.SECTION
    assert tokenizer.tokens[1].kind == TokenKind.PARAMETER
