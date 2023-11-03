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
        return self._default_section[key]

    def __setitem__(self, key, value):
        # Add a new parameter in the default section, but first make sure there is no section
        # with the same name.
        if key in self._sections:
            raise ValueError(f"Section '{key}' already exists")
        self._default_section[key] = value

    def to_str(self) -> str:
        result = ""

        # Write the default section
        for key, value in self._default_section.items():
            result += f"{key} = {value}\n"
        result += "\n"

        # Write remaining sections
        for section, parameters in self._sections.items():
            result += f"[{section}]\n"
            for key, value in parameters.items():
                result += f"{key} = {value}\n"
            result += "\n"
    
        # Ensure there is only one newline at the end of the file
        return result.rstrip("\n") + "\n"
