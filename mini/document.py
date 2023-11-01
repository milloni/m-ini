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
        # Cf __getitem__
        # TODO error handle if a section with this name exists
        self._default_section[key] = value
