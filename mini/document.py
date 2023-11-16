import json
from typing import Dict


class IniDocument:
    """
    An object of this class represents an INI config. It is essentially an unordered mapping of
    key/value pairs, which may be grouped into sections.

    These key/value pairs are called "properties" and are always of type str. For simplicity, we do
    not attempt to parse the values into other types, such as int or bool.

    Properties that do not belong to any section are called "global properties".

    The user can access properties through a dict-like interface, by referring to the property name
    or a section name, in a nested way. For example:

    doc["language"] -> global property "language"
    doc["pet"]["name"] -> property "name" in section "pet"
    """

    def __init__(self) -> None:
        self._sections: Dict[str, Dict[str, str]] = {}
        self._default_section: Dict[str, str] = {}

    def add_section(self, name: str) -> None:
        """Add a new section to the config."""
        self._sections[name] = {}

    def get_section(self, name: str) -> Dict[str, str]:
        """Access a section by name."""

        if name not in self._sections:
            raise KeyError(f"Section '{name}' does not exist")
        return self._sections[name]

    def __getitem__(self, key: str) -> Dict[str, str] | str:
        """Access a section or a global property."""

        # This could be either a section, or a property in the default section
        if key in self._sections:
            return self._sections[key]
        return self._default_section[key]

    def __setitem__(self, key: str, value: str) -> None:
        """Set a global property."""

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
        result = IniDocument._write_section(self._default_section)
        for section_name, section in self._sections.items():
            result += IniDocument._write_section(section, section_name)
        # Ensure there is only one newline at the end of the file
        return result.rstrip("\n") + "\n"

    def to_json(self) -> str:
        """Return a JSON representation of the config."""
        d = self._default_section | self._sections
        return json.dumps(d, indent=2)

    @staticmethod
    def _write_section(section: Dict[str, str], section_name: str | None = None) -> str:
        result = ""
        # Add section header
        if section_name:
            result += f"[{section_name}]\n"

        # Add section properties
        result += "\n".join(f"{key} = {value}" for key, value in section.items())

        # Sections are separated by blank lines
        if section:
            result += "\n\n"
        return result
