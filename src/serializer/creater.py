from .base import BaseSerializer
from .json import JsonSerializer
from .yaml import YamlSerializer
from .toml import TomlSerializer


class Serializers:
    __serializers = {
        "json": JsonSerializer(),
        "yaml": YamlSerializer(),
        "toml": TomlSerializer(),
    }
    @classmethod
    def create_serializer(cls, name: str) -> BaseSerializer:
        if name in cls.__serializers:
            return cls.__serializers[name]
