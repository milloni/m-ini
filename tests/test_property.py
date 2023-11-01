from mini.property import Property


def test_property():
    prop = Property.from_str("name = Leon")
    assert prop.key == "name"
    assert prop.value == "Leon"


def test_property2():
    prop = Property.from_str("name=Leon")
    assert prop.key == "name"
    assert prop.value == "Leon"


def test_property3():
    prop = Property.from_str(" name = Leon ")
    assert prop.key == "name"
    assert prop.value == "Leon"