import importlib.util
import inspect
import sys
import types
import re

from src.dto import DtoTypes, Dto
from src.parser import YamlParser


class YamlService:

    __gaps = []
    __gaps_blocked = False
    __result = ""
    __parser = None

    def __init__(self):
        self.__parser = YamlParser()

    def serializer(self, obj):
        self.__result = ""
        self._visit(obj, first_call=True)
        self.__result = re.sub(r"(\n)\1+", "\n", self.__result)
        return self.__result

    def deserialize(self, s: str):
        return self.__parser.parse(s)

    def _put(self, s: str, gaps: bool = False):
        if gaps and not self.__gaps_blocked:
            self.__result += "".join(self.__gaps)
        self.__result += s
        self.__gaps_blocked = False

    def _push_gap(self, gap: str = "  "):
        self.__gaps.append(gap)

    def _pop_gap(self):
        return self.__gaps.pop()

    def _block_gaps(self):
        self.__gaps_blocked = True

    def _is_primitive_type(self, obj):
        return type(obj) in (int, float, str, bool, bytes)

    def _visit_primitive(self, obj):
        if type(obj) in (int, float):
            self._put(f'{obj}')
        elif type(obj) == str:
            self._put(f'"{obj}"')
        elif type(obj) == bool:
            value = ""
            if obj:
                value = "true"
            else:
                value = "false"
            self._put(f'{value}')
        elif type(obj) == bytes:
            encoded = obj.hex()
            self._put(f'"{encoded}"')

    def _visit_dict(self, _dict: dict):
        self._put(f'{Dto.dto_type}: "{DtoTypes.DICT}"\n', gaps=True)
        for item in _dict.items():
            self._put(f'{item[0]}: ', gaps=True)
            self._visit(item[1])
            self._put("\n")

    def _visit_list(self, _list: list):
        if len(_list) >= 1:
            for item in _list:
                self._put("- ", gaps=True)
                if not self._is_primitive_type(item):
                    self._block_gaps()
                self._visit(item, new_line=False)
                self._put("\n")
        else:
            self.__result = self.__result[: -1]
            self._put("[]")

    def _visit_func(self, func):
        self._put(f'{Dto.dto_type}: "{DtoTypes.FUNC}"\n', gaps=True)
        self._put(f'{Dto.name}: "{func.__name__}"\n', gaps=True)
        self._put(f'{Dto.global_names}:', gaps=True)
        self._visit_func_globals(func)
        self._put(f'{Dto.code}: ', gaps=True)
        self._visit(func.__code__)

    def _visit_func_globals(self, func):
        code = func.__code__
        func_globals = func.__globals__.items()
        actual_globals = {}
        for glob in func_globals:
            if glob[0] in code.co_names:
                actual_globals.update({glob[0]: glob[1]})
        self._visit(actual_globals)

    def _visit_func_code(self, code):
        self._put(f'{Dto.dto_type}: "{DtoTypes.CODE}"\n', gaps=True)
        self._put(f'{Dto.fields}:', gaps=True)
        code_dict = {}
        for member in inspect.getmembers(code):
            if str(member[0]).startswith("co_"):
                code_dict.update({member[0]: member[1]})
        self._visit(code_dict)

    def _visit_module(self, module):
        module_fields = {}
        self._put(f'{Dto.dto_type}: "{DtoTypes.MODULE}"\n', gaps=True)
        self._put(f'{Dto.name}: "{module.__name__}"\n', gaps=True)
        self._put(f'{Dto.fields}:', gaps=True)

        is_std_lib_module = False
        python_libs_path = sys.path[2]
        module_path = importlib.util.find_spec(module.__name__)[1]
        if module.__name__ in sys.builtin_module_names:
            is_std_lib_module = True
        elif python_libs_path in module_path:
            is_std_lib_module = True
        elif 'site-packages' in module_path:
            is_std_lib_module = True
        if is_std_lib_module:
            self._visit(None)
        else:
            module_members = inspect.getmembers(module)
            for mem in module_members:
                if not mem[0].startswith("__"):
                    module_fields.update({mem[0]: mem[1]})
        self._visit(module_fields)

    def _visit_class(self, _class):
        self._put(f'{Dto.dto_type}: "{DtoTypes.CLASS}"\n', gaps=True)
        self._put(f'{Dto.name}: "{_class.__name__}"\n', gaps=True)
        self._put(f'{Dto.fields}:', gaps=True)

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
                            "__mro__", "__base__", "__basicsize__",
                            "__class__", "__dictoffset__", "__name__",
                            "__qualname__", "__text_signature__", "__itemsize__",
                            "__flags__", "__weakrefoffset__"
                    ):
                        fields_dict.update({mem[0]: mem[1]})
        self._visit(fields_dict)

    def _visit_obj(self, obj):
        self._put(f'{Dto.dto_type}: "{DtoTypes.OBJ}"\n', gaps=True)
        self._put(f'{Dto.base_class}:', gaps=True)
        self._visit(obj.__class__)
        self._put(f'{Dto.fields}:', gaps=True)
        self._visit(obj.__dict__)

    def _visit(self, obj, first_call: bool = False, new_line: bool = True):
        if not first_call:
            self._push_gap()
        else:
            pass

        if self._is_primitive_type(obj):
            self._visit_primitive(obj)
        elif obj is None:
            self._put('null')
        else:
            if len(self.__gaps) >= 1 and new_line:
                self._put("\n")
            if type(obj) == dict:
                self._visit_dict(obj)
            elif type(obj) in (tuple, list):
                self._visit_list(list(obj))
            elif inspect.isclass(obj):
                self._visit_class(obj)
            elif type(obj) == types.CodeType:
                self._visit_func_code(obj)
            elif type(obj) == types.ModuleType:
                self._visit_module(obj)
            elif callable(obj):
                self._visit_func(obj)
            elif isinstance(obj, object):
                self._visit_obj(obj)
        if not first_call:
            self._pop_gap()
        else:
            pass
