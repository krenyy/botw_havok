import os


class Messages:
    @staticmethod
    def loading(file: str):
        print(f"{bcolors.OKBLUE}Loading '{os.path.basename(file)}'{bcolors.ENDC}")

    @staticmethod
    def writing(file: str):
        print(f"{bcolors.OKBLUE}Writing '{os.path.basename(file)}'{bcolors.ENDC}")

    @staticmethod
    def done():
        print(f"{bcolors.OKGREEN}Done!{bcolors.ENDC}")


def check_if_exists(file: str):
    if os.path.isfile(file):
        choice = input(
            f"{bcolors.WARNING}'{os.path.basename(file)}' exists, do you wish to overwrite it?{bcolors.ENDC}\n$ "
        ).upper()
        if choice.startswith("Y"):
            pass
        else:
            raise SystemExit(f"{bcolors.FAIL}Operation aborted!{bcolors.ENDC}")


def change_extension(file: str, extension: str) -> str:
    return f'{".".join(file.split(".")[:-1])}.{extension}'


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
