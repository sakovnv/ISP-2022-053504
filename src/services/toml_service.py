import importlib
import inspect
import sys
import types

from src.dto import DtoTypes, Dto
from src.parser import TomlParser


class TomlService:

    __result = ""
    __names_container = []
    __parser = None

    def __init__(self):
        self.__parser = TomlParser()

    def serialize(self, obj):
        self.__result = ""
        self._visit(obj)
        return self.__result

    def deserialize(self, s: str):
        return self.__parser.parse(s)

    def _put(self, s: str):
        self.__result += s

    def _push_name(self, s: str):
        self.__names_container.append(s)

    def _pop_name(self) -> str:
        return self.__names_container.pop()

    def _get_concat_name(self) -> str:
        return (".".join(self.__names_container))[1:]

    def _visit(self, obj, new_name: str = ""):
        if self._is_primitive_type(obj):
            self._visit_primitive(obj)
        else:
            self._visit_complex(obj, new_name)

    def _is_primitive_type(self, obj: any) -> bool:
        _type = type(obj)
        if _type in (int, float, str, bool, bytes) or obj is None:
            return True
        elif _type in (tuple, list):
            if len(obj) >= 1:
                return False
            else:
                return True
        return False

    def _visit_primitive(self, prim_obj):
        _type = type(prim_obj)
        if _type in (int, float):
            self._put(f'{prim_obj}')
        elif _type == str:
            self._put(f'"{prim_obj}"')
        elif _type == bool:
            val = "true" if prim_obj else "false"
            self._put(f'{val}')
        elif prim_obj is None:
            self._put("{}")
        elif type(prim_obj) in (tuple, list) and len(prim_obj) == 0:
            self._put("[]")
            return
        elif _type == bytes:
            encoded = prim_obj.hex()
            self._put(f'"{encoded}"')

    def _visit_complex(self, comp_obj: any, name_container: str):
        self._push_name(name_container)
        name = self._get_concat_name()
        if len(self.__names_container) > 1:
            self._put(f'[{name}]\n')
        if type(comp_obj) == dict:
            self._visit_dict(comp_obj)
        elif type(comp_obj) in (tuple, list):
            self._visit_list(comp_obj)
        elif type(comp_obj) == types.ModuleType:
            self._visit_module(comp_obj)
        elif inspect.isclass(comp_obj):
            self._visit_class(comp_obj)
        elif type(comp_obj) == types.CodeType:
            self._visit_func_code(comp_obj)
        elif callable(comp_obj):
            self._visit_func(comp_obj)
        elif isinstance(comp_obj, object):
            self._visit_obj(comp_obj)

        self._pop_name()

    def _visit_dict(self, _dict: dict):
        prim_dict, complex_dict = self._divide_dict_by_primitive(_dict)

        self._put(f'{Dto.dto_type} = "{DtoTypes.DICT}"\n')

        for prim in prim_dict.items():
            self._put(f'{prim[0]} = ')
            self._visit(prim[1])
            self._put("\n")

        self._put("\n")

        for comp in complex_dict.items():
            self._visit(comp[1], comp[0])
            self._put("\n")

    def _visit_list(self, _list: any):
        prim_list, complex_list = self._divide_list_by_primitive(_list)
        self._put(f'{Dto.dto_type} = "{DtoTypes.LIST}"\n')
        i = 0
        for prim in prim_list:
            self._put(f'{Dto.item}{i} = ')
            self._visit(prim)
            self._put("\n")
            i += 1
        self._put("\n")
        for comp in complex_list:
            self._visit(comp, f'{Dto.item}{i}')
            self._put("\n")
            i += 1

    def _visit_module(self, module):
        self._put(f'{Dto.dto_type} = "{DtoTypes.MODULE}"\n')
        self._put(f'{Dto.name} = "{module.__name__}"\n')
        if self._is_std_lib_module(module):
            self._put(f'{Dto.fields} = ')
            self._visit(None)
            self._put("\n")
        else:
            self._put("\n")
            module_fields = self._get_actual_module_fields(module)
            self._visit(module_fields, Dto.fields)

    def _divide_list_by_primitive(self, _list: list) -> tuple:
        prim_list = []
        complex_list = []
        for item in _list:
            if self._is_primitive_type(item):
                prim_list.append(item)
            else:
                complex_list.append(item)
        return prim_list, complex_list

    def _divide_dict_by_primitive(self, _dict: dict) -> tuple:
        prim_dict = {}
        complex_dict = {}
        for item in _dict.items():
            if self._is_primitive_type(item[1]):
                prim_dict.update({item[0]: item[1]})
            else:
                complex_dict.update({item[0]: item[1]})
        return prim_dict, complex_dict

    def _visit_class(self, _class):
        self._put(f'{Dto.dto_type} = "{DtoTypes.CLASS}"\n')
        self._put(f'{Dto.name} = "{_class.__name__}"\n\n')
        # self._put(f'"{Dto.fields}": ')
        fields_dict = self._get_actual_class_fields(_class)
        self._visit(fields_dict, Dto.fields)

    def _visit_func_code(self, func):
        self._put(f'{Dto.dto_type} = "{DtoTypes.CODE}"\n\n')
        code_dict = self._get_actual_code_fields(func)
        self._visit(code_dict, Dto.fields)

    def _visit_func(self, func):
        self._put(f'{Dto.dto_type} = "{DtoTypes.FUNC}"\n')
        self._put(f'{Dto.name} = "{func.__name__}"\n\n')
        self._visit_func_globals(func)
        self._visit(func.__code__, Dto.code)

    def _visit_func_globals(self, func):
        actual_globals = self._get_actual_func_globals(func)
        self._visit(actual_globals, Dto.global_names)

    def _visit_obj(self, obj):
        self._put(f'{Dto.dto_type} =  "{DtoTypes.OBJ}"\n\n')
        self._visit(obj.__class__, Dto.base_class)
        self._visit(obj.__dict__, Dto.fields)

    def _get_actual_func_globals(self, func) -> dict:
        code = func.__code__
        func_globals = func.__globals__.items()
        actual_globals = {}
        for glob in func_globals:
            if glob[0] in code.co_names:
                actual_globals.update({glob[0]: glob[1]})
        return actual_globals

    def _get_actual_code_fields(self, _code: types.CodeType) -> dict:
        code_dict = {}
        for member in inspect.getmembers(_code):
            if str(member[0]).startswith("co_"):
                code_dict.update({member[0]: member[1]})
        return code_dict

    def _get_actual_module_fields(self, module: types.ModuleType) -> dict:
        module_fields = {}
        module_members = inspect.getmembers(module)
        for mem in module_members:
            if not mem[0].startswith("__"):
                module_fields.update({mem[0]: mem[1]})
        return module_fields

    def _get_actual_class_fields(self, _class: type) -> dict:
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
        return fields_dict

    def _is_std_lib_module(self, module: types.ModuleType):
        python_libs_path = sys.path[2]
        module_path = importlib.import_module(module.__name__)[1]
        print(module_path)
        if module.__name__ in sys.builtin_module_names:
            return True
        elif python_libs_path in module_path:
            return True
        elif 'site-packages' in module_path:
            return True
        return False
