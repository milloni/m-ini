import os
import pathlib
import pytest
from mini.document import IniDocument

data_path = pathlib.Path(os.path.dirname(__file__)).joinpath("data")


@pytest.fixture
def ini_doc(request):
    if request.param == "hello":
        doc = IniDocument()
        doc.add_section("pet")
        doc["pet"]["name"] = "Leon"
        doc["pet"]["species"] = "cat"
        doc["language"] = "Polish"
        doc["location"] = "Poland"

    elif request.param == "only_default_section":
        doc = IniDocument()
        doc["language"] = "Polish"
        doc["location"] = "Poland"

    elif request.param == "many_sections":
        doc = IniDocument()
        doc.add_section("London")
        doc["London"]["population"] = "8900000"
        doc["London"]["region"] = "Greater London"
        doc.add_section("Birmingham")
        doc["Birmingham"]["population"] = "1100000"
        doc["Birmingham"]["region"] = "West Midlands"
        doc.add_section("Manchester")
        doc["Manchester"]["population"] = "550000"
        doc["Manchester"]["region"] = "Greater Manchester"
        doc.add_section("Glasgow")
        doc["Glasgow"]["population"] = "600000"
        doc["Glasgow"]["region"] = "Scotland"

    return doc


@pytest.mark.parametrize("ini_doc", ["hello"], indirect=["ini_doc"])
def test_document(ini_doc):
    assert ini_doc["pet"]["name"] == "Leon"
    assert ini_doc["pet"]["species"] == "cat"
    assert ini_doc["language"] == "Polish"
    assert ini_doc["location"] == "Poland"


@pytest.mark.parametrize("ini_doc", ["hello"], indirect=["ini_doc"])
def test_name_clash(ini_doc):
    # Attempt to add a parameter where as a section with the same name
    # exists - this is not allowed.
    with pytest.raises(ValueError):
        ini_doc["pet"] = "I like cats"
    # Overwriting a parameter should be fine
    ini_doc["pet"]["name"] = "Bimba"
    assert ini_doc["pet"]["name"] == "Bimba"


@pytest.mark.parametrize(
    "ini_doc, filename_expected", [
        ("hello", "hello.ini"),
        ("only_default_section", "only_default_section.ini"),
        ("many_sections", "many_sections.ini")
    ], indirect=["ini_doc"]
)
def test_serialize(ini_doc, filename_expected):
    # Compare serialized output with expected text
    expected_text_path = data_path.joinpath(filename_expected)
    with open(expected_text_path, "r", encoding="utf-8") as f:
        expected_text = f.read()
    text = ini_doc.to_str()
    assert text == expected_text


@pytest.mark.parametrize(
    "ini_doc, filename_expected",
    [("hello", "hello.json")],
    indirect=["ini_doc"]
)
def test_json(ini_doc, filename_expected):
    # Read expected JSON from file and compare with the output.
    json_path = data_path.joinpath(filename_expected)
    with open(json_path, "r", encoding="utf-8") as f:
        expected_json = f.read().strip()
    assert ini_doc.to_json() == expected_json
