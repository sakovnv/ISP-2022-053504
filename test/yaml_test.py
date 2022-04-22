from unittest import TestCase, main
from src import YamlSerializer
from test import tested_data as data

serializer = YamlSerializer()

FILE_PATH = "/home/sakovnv/PycharmProjects/ISP-Lab-2/file.yaml"


class YamlTest(TestCase):

    def test_instance(self):
        obj1 = data.TestClass(7)
        ser_obj = serializer.loads(serializer.dumps(data.TestClass(7)))
        self.assertEqual(obj1.get_value(), ser_obj.get_value())

    def test_func(self):
        func = serializer.loads(serializer.dumps(data.test_func))
        self.assertEqual(func(5), data.test_func(5))

    def test_obj(self):
        obj1 = data.TestClass(7)
        ser_obj = serializer.loads(serializer.dumps(data.test_obj))
        ser_obj.set_value(7)
        self.assertEqual(obj1.get_value(), ser_obj.get_value())

    def test_to_file(self):
        obj = data.test_func
        serializer.dump(obj, FILE_PATH)
        self.assertEqual(obj(5), 25)

    def test_from_file(self):
        obj = serializer.load(FILE_PATH)
        self.assertIsNotNone(obj)


if __name__ == "__main__":
    main()
