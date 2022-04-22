from abc import ABC, abstractmethod


class BaseSerializer(ABC):

    @abstractmethod
    def dump(self, obj, fp: str):
        pass

    @abstractmethod
    def dumps(self, obj) -> str:
        pass

    @abstractmethod
    def load(self, fp: str):
        pass

    @abstractmethod
    def loads(self, s: str):
        pass
