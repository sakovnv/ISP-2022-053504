class TestClass:
    __value = None
    __items: list = []

    def __init__(self, val: int = 0):
        self.__value = val

    def get_value(self):
        return self.__value

    def set_value(self, val: int):
        self.__value = val

    def add_item(self, elem):
        self.__items.append(elem)
        return self.__items

    def get_items(self):
        return self.__items


def test_func(num: int):
    return num**2


test_obj = TestClass()

