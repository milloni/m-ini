class IniDocument:
    def __init__(self):
        self._sections = {}
        self._default_section = {}

    def add_section(self, name: str):
        self._sections[name] = {}

    def __getitem__(self, key: str) -> dict:
        # This could be either a section, or a parameter in the default section
        if key in self._sections:
            return self._sections[key]
        else:
            return self._default_section[key]

    def __setitem__(self, key, value):
        # Add a new parameter in the default section, but first check if a such with# the same
        # name doesn't exist
        if key in self._sections:
            raise ValueError(f"Section '{key}' already exists")
        self._default_section[key] = value
    
    def to_str(self) -> str:
        result = ""

        # Write the default section
        for parameter in self._default_section:
            result += f"{parameter} = {self._default_section[parameter]}\n"
        result += "\n"

        # Write remaining sections
        for section in self._sections:
            result += f"[{section}]\n"
            for parameter in self._sections[section]:
                result += f"{parameter} = {self._sections[section][parameter]}\n"
            result += "\n"
        return result
        # TODO: fix spurious newline at the end