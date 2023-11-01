import re

class Property:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value
    
    @classmethod
    def from_str(cls, data: str):
        key, value = data.split("=")
        return cls(key.strip(), value.strip())