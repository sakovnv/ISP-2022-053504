import inspect
import types

from src.dto import DtoTypes, Dto
from src.parser import JsonParser


class JsonService:

    __result = ""
    __parser = None

    def __init__(self):
        self.__parser = JsonParser()

    def serialize(self, obj):
        self.__result = ""
        self._visit(obj)
        return self.__result

    def deserialize(self, s: str):
        return self.__parser.parse(s)

    def _put(self, s: str):
        self.__result += s

    def _visit_primitive_type(self, obj):
        if type(obj) in (int, float):
            self._put(f'{obj}')
        elif type(obj) == str:
            self._put(f'"{obj}"')
        elif type(obj) == bool:
            self._put(f'{str(obj).lower()}')
        elif type(obj) in (list, tuple):
            self._put('[')
            for i, i_obj in enumerate(obj):
                if i != 0:
                    self._put(',')
                self._visit(i_obj)
            self._put(']')
        elif type(obj) == bytes:
            self._put(f'"{obj.hex()}"')

    def _visit_dict(self, _dict: dict):
        self._put(f'"{Dto.dto_type}": "{DtoTypes.DICT}"')
        if len(_dict.items()) >= 1:
            self._put(",")
        is_first = True
        for item in _dict.items():
            if not is_first:
                self._put(',')
            self._put(f'"{item[0]}": ')
            self._visit(item[1])
            is_first = False

    def _visit_module(self, module):
        module_fields = {}
        self._put(f'"{Dto.dto_type}": {DtoTypes.MODULE}",')
        self._put(f'"{Dto.name}": "{module.__name__}",')
        self._put(f'"{Dto.fields}": ')
        module_members = inspect.getmembers(module)
        for mem in module_members:
            if not mem[0].startswith("__"):
                module_fields.update({mem[0]: mem[1]})
        self._visit(module_fields)

    def _visit_class(self, _class):
        self._put(f'"{Dto.dto_type}": "{DtoTypes.CLASS}",')
        self._put(f'"{Dto.name}": "{_class.__name__}",')
        self._put(f'"{Dto.fields}": ')
        fields_dict = {}
        if _class == type:
            fields_dict.update({
                "__bases__": [],
            })
        else:
            mems = inspect.getmembers(_class)
            for mem in mems:
                if type(mem[1]) not in (
                    types.WrapperDescriptorType,
                    types.MethodDescriptorType,
                    types.BuiltinFunctionType,
                    types.MappingProxyType,
                    types.GetSetDescriptorType
                ):
                    if mem[0] not in (
                        "__mro__", "__base__", "__basicsize__", "__class__",
                        "__dictoffset__", "__name__", "__qualname__", "__text_signature__",
                        "__itemsize__", "__flags__", "__weakrefoffset__"
                    ):
                        fields_dict.update({mem[0]: mem[1]})
        self._visit(fields_dict)

    def _visit_func(self, func):
        self._put(f'"{Dto.dto_type}": "{DtoTypes.FUNC}",')
        self._put(f'"{Dto.name}": "{func.__name__}",')
        self._put(f'"{Dto.global_names}": ')
        self._visit_func_globals(func)
        self._put(',')
        self._put(f'"{Dto.code}": ')
        self._visit(func.__code__)

    def _visit_func_globals(self, func):
        code = func.__code__
        func_globals = func.__globals__.items()
        actual_globals = {}
        for glob in func_globals:
            if glob[0] in code.co_names:
                actual_globals.update({glob[0]: glob[1]})
        self._visit(actual_globals)

    def _visit_func_code(self, code: types.CodeType):
        self._put(f'"{Dto.dto_type}": "{DtoTypes.CODE}",')
        self._put(f'"{Dto.fields}":')
        code_dict = {}
        for member in inspect.getmembers(code):
            if str(member[0]).startswith("co_"):
                code_dict.update({member[0]: member[1]})
        self._visit(code_dict)

    def _visit_obj(self, obj):
        self._put(f'"{Dto.dto_type}": "{DtoTypes.OBJ}",')
        self._put(f'"{Dto.base_class}": ')
        self._visit(obj.__class__)
        self._put(',')
        self._put(f'"{Dto.fields}": ')
        self._visit(obj.__dict__)

    def _visit(self, obj):
        if obj is None:
            self._put("{}")
        elif type(obj) in (int, float, str, bool, bytes, tuple, list):
            self._visit_primitive_type(obj)
        else:
            self._put('{')
            if type(obj) == dict:
                self._visit_dict(obj)
            elif type(obj) == types.CodeType:
                self._visit_func_code(obj)
            elif type(obj) == types.ModuleType:
                self._visit_module(obj)
            elif inspect.isclass(obj):
                self._visit_class(obj)
            elif callable(obj):
                self._visit_func(obj)
            elif isinstance(obj, object):
                self._visit_obj(obj)
            self._put('}')
