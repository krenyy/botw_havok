import os

from colorama import Fore, init

from .. import Havok
from ..binary.types import String

templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")


class Messages:
    @staticmethod
    def loading(file: str):
        print(f"{Fore.BLUE}Loading '{os.path.basename(file)}' to memory")

    @staticmethod
    def writing(file: str):
        print(f"{Fore.BLUE}Writing '{os.path.basename(file)}'")

    @staticmethod
    def serializing(file: str):
        print(f"{Fore.BLUE}Serializing '{os.path.basename(file)}'")

    @staticmethod
    def deserializing(file: str):
        print(f"{Fore.BLUE}Deserializing '{os.path.basename(file)}'")

    @staticmethod
    def done():
        print(f"{Fore.GREEN}Done!")


def check_if_exists(file: str):
    if os.path.isfile(file):
        choice = input(
            f"{Fore.YELLOW}'{os.path.basename(file)}' exists, do you wish to overwrite it?\n$ "
        ).upper()
        if choice.startswith("Y"):
            pass
        else:
            raise SystemExit(f"{Fore.RED}Operation aborted!")


def change_extension(file: str, extension: str) -> str:
    return f'{".".join(file.split(".")[:-1])}.{extension}'
