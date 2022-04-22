import argparse
import configparser
import os.path

from src.serializer.creater import Serializers


class CommandLineInterface:

    __parser = None
    __args = None

    def args_init(self):
        self.__parser = argparse.ArgumentParser()
        self.__parser.add_argument('--f', '--from', type=str, help="source file path for converting")
        self.__parser.add_argument('--t', '--to', type=str, help="file path")
        self.__parser.add_argument('--C', '--config', type=str, help="path to config file")
        self.__args = self.__parser.parse_args()

    def execution(self):
        source_file, to_file = None, None
        if self.__args.C is not None:
            source_file, to_file = os.path.abspath(self._get_config())
        else:
            source_file = os.path.abspath(self.__args.f)
            to_file = os.path.abspath(self.__args.t)

        self._converting(source_file, to_file)

    def _converting(self, source_file: str, to_file: str):
        if source_file is not None and to_file is not None:
            source_format = source_file.split('.')[1]
            to_format = to_file.split('.')[1]

            source_serializer = Serializers.create_serializer(source_format)
            to_serializer = Serializers.create_serializer(to_format)

            obj = source_serializer.load(source_file)
            to_serializer.dump(obj, to_file)
        else:
            self.__parser.error(f"args: --f from | --t to | --C config")

    def _get_config(self) -> tuple:
        config_path = self.__args.C
        if os.path.exists(config_path):
            config = configparser.RawConfigParser()
            config.read(config_path)
            source_file = config["FILE_PATHS"][self.__args.f]
            to_file = config["FILE_PATHS"][self.__args.f]
            return source_file, to_file
        else:
            self.__parser.error("incorrect config file path")
