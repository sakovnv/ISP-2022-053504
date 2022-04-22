from src.serializer.base import BaseSerializer
from src.services import YamlService


class YamlSerializer(BaseSerializer):

    __service = None

    def __init__(self):
        self.__service = YamlService()

    def dump(self, obj, fp: str):
        file = open(fp, 'w')
        file.write(self.dumps(obj))
        file.close()

    def dumps(self, obj) -> str:
        return self.__service.serializer(obj)

    def load(self, fp: str):
        file = open(fp, 'r')
        file_str = file.read()
        file.close()
        return self.loads(file_str)

    def loads(self, s: str):
        obj = self.__service.deserialize(s)
        return obj
