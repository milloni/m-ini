import json

class IniDocument:
    """
    An object of this class represents an INI config. It is essentially an unordered mapping of
    key/value pairs, which may be grouped into sections.

    These key/value pairs are called "properties" and are always of type str. For simplicity, we do
    not attempt to parse the values into other types, such as int or bool.

    Properties that do not belong to any section are called "global properties".

    The user can access properties through a dict-like interface, by referring to the property name
    or a section name, in a nested way. For example:

    doc["language"] -> property "language" in the default section
    doc["pet"]["name"] -> property "name" in section "pet"
    """

    def __init__(self):
        self._sections = {}
        self._default_section = {}

    def add_section(self, name: str):
        """Add a new section to the config."""
        self._sections[name] = {}

    def __getitem__(self, key: str) -> dict:
        """Access a section or a global property."""

        # This could be either a section, or a property in the default section
        if key in self._sections:
            return self._sections[key]
        return self._default_section[key]

    def __setitem__(self, key: str, value: str):
        "Set a global property."

        # Add a new property in the default section, but first make sure there is no section
        # with the same name.
        if key in self._sections:
            raise ValueError(f"Section '{key}' already exists")
        self._default_section[key] = value

    def to_str(self) -> str:
        """
        Return a string representation of the config. Use this function when you want to store
        the config in an INI file.
        """

        result = ""

        # Write the default section
        for key, value in self._default_section.items():
            result += f"{key} = {value}\n"
        if self._default_section:
            result += "\n"

        # Write remaining sections
        for section, properties in self._sections.items():
            result += f"[{section}]\n"
            for key, value in properties.items():
                result += f"{key} = {value}\n"
            result += "\n"

        # Ensure there is only one newline at the end of the file
        return result.rstrip("\n") + "\n"

    def to_json(self) -> str:
        """Return a JSON representation of the config."""
        d = self._default_section | self._sections
        return json.dumps(d, indent=2)
