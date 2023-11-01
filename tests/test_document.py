import pytest
from mini.document import IniDocument


def test_document():
    doc = IniDocument()
    doc.add_section("pets")
    doc["pets"]["name"] = "Leon"
    doc["pets"]["species"] = "cat"
    doc["language"] = "Polish"
    doc["location"] = "Poland"

    assert doc["pets"]["name"] == "Leon"
    assert doc["pets"]["species"] == "cat"
    assert doc["language"] == "Polish"
    assert doc["location"] == "Poland"


def test_serialize():
    pass