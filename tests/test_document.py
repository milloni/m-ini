import os
import pathlib
import pytest
from mini.document import IniDocument

data_path = pathlib.Path(os.path.dirname(__file__)).joinpath("data")


@pytest.fixture
def hello_doc(request):
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


@pytest.mark.parametrize("hello_doc", ["hello"], indirect=["hello_doc"])
def test_document(hello_doc):
    assert hello_doc["pet"]["name"] == "Leon"
    assert hello_doc["pet"]["species"] == "cat"
    assert hello_doc["language"] == "Polish"
    assert hello_doc["location"] == "Poland"


@pytest.mark.parametrize("hello_doc", ["hello"], indirect=["hello_doc"])
def test_name_clash(hello_doc):
    # Attempt to add a parameter where as a section with the same name
    # exists - this is not allowed.
    with pytest.raises(ValueError):
        hello_doc["pet"] = "I like cats"
    # Overwriting a parameter should be fine
    hello_doc["pet"]["name"] = "Bimba"
    assert hello_doc["pet"]["name"] == "Bimba"


@pytest.mark.parametrize(
    "hello_doc, filename_expected", [
        ("hello", "hello.ini"),
        ("only_default_section", "only_default_section.ini"),
        ("many_sections", "many_sections.ini")
    ], indirect=["hello_doc"]
)
def test_serialize(hello_doc, filename_expected):
    # Compare serialized output with expected text
    expected_text_path = data_path.joinpath(filename_expected)
    with open(expected_text_path, "r", encoding="utf-8") as f:
        expected_text = f.read()
    text = hello_doc.to_str()
    assert text == expected_text


@pytest.mark.parametrize(
    "hello_doc, filename_expected",
    [("hello", "hello.json")],
    indirect=["hello_doc"]
)
def test_json(hello_doc, filename_expected):
    # Read expected JSON from file and compare with the output.
    json_path = data_path.joinpath(filename_expected)
    with open(json_path, "r", encoding="utf-8") as f:
        expected_json = f.read().strip()
    assert hello_doc.to_json() == expected_json
