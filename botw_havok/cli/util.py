import os
from colorama import init, Fore

init()


class Messages:
    @staticmethod
    def loading(file: str):
        print(f"{Fore.BLUE}Loading '{os.path.basename(file)}'")

    @staticmethod
    def writing(file: str):
        print(f"{Fore.BLUE}Writing '{os.path.basename(file)}'")

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
