from src import JsonSerializer, YamlSerializer, TomlSerializer
from test import tested_data as data


def some_func(obj):
    test = Test()
    print("This is function " + obj)
    return test


class Test:
    name = "petya"
    age = 19
    height = 90
    collect = ["hes", "wdaw", "dwww"]
    DICT = {"1": 1, "2": 2}


def main():
    val = Test()
    print(val.name)
    value = {"sorak": 40, "dvacac'": 20, "desyat": 10}

    test = data.TestClass()
    print(test.get_value())
    JsonSerializer().dump(test, 'file.json')
    YamlSerializer().dump(val, 'file.yaml')
    TomlSerializer().dump(val, 'file.toml')

    obj1 = data.TestClass(7)
    ser_obj = JsonSerializer().loads(JsonSerializer().dumps(data.TestClass(7)))
    # print(ser_obj.get_value())
    # print(YamlSerializer().load("file.yaml"))
    # a = Animal()
    # print(id(a))
    # print("---------------")
    # print(id(b))
    # print(id(a) == id(b))


if __name__ == "__main__":
    main()
