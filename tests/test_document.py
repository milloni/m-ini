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
    pass