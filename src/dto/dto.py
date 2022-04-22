from dataclasses import dataclass


@dataclass
class DtoTypes:
    FUNC = "func"
    MODULE = "module"
    CLASS = "class"
    OBJ = "obj"
    DICT = "dict"
    CODE = "code"
    LIST = "list"


@dataclass
class Dto:
    dto_type = "DTO_TYPE"
    name = "name"
    fields = "fields"
    path = "path"
    code = "code"
    global_names = "globals"
    base_class = "class"
    item = "__dto__list_dict_item"
