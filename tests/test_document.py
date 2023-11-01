import pytest
from mini.document import IniDocument
import pathlib
import os

data_path = pathlib.Path(os.path.dirname(__file__)).joinpath("data")

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


def test_name_clash():
    doc = IniDocument()
    doc.add_section("pets")
    doc["pets"]["name"] = "Leon"
    doc["pets"]["species"] = "cat"
    doc["language"] = "Polish"
    doc["location"] = "Poland"

    # We should get an error when parameter name clashes with section name
    with pytest.raises(ValueError):
        doc["pets"] = "I like pets"
    # Overwriting a parameter should be fine
    doc["pets"]["name"] = "Bimba"
    assert doc["pets"]["name"] == "Bimba"


def test_serialize():
    doc = IniDocument()
    doc.add_section("pets")
    doc["pets"]["name"] = "Leon"
    doc["pets"]["species"] = "cat"
    doc["language"] = "Polish"
    doc["location"] = "Poland"

    # Compare serialized output with expected text
    expected_text_path = data_path.joinpath("hello.ini")
    with open(expected_text_path, "r") as f:
        expected_text = f.read()
    text = doc.to_str()
    print(text)
    assert text == expected_text