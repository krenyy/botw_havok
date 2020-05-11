import argparse

from .. import Havok
from .common import Fore, Messages, change_extension, check_if_exists, init


def parse_args():
    parser = argparse.ArgumentParser(description="Convert Havok JSON file to packfile")
    parser.add_argument("jsonFile", help="Path to destination JSON file")
    parser.add_argument("outFile", help="Path to a Havok packfile", nargs="?")
    parser.add_argument(
        "-nx", "--switch", action="store_true", help="Use to output the file for Switch"
    )

    return parser.parse_args()


def json_to_hk(jsonFile: str, outFile: str, nx: bool):
    Messages.loading(jsonFile)
    hk = Havok.from_json(jsonFile)

    if not outFile:
        outFile = change_extension(jsonFile, hk.guess_extension())

        check_if_exists(outFile)

    if nx:
        print(f"{Fore.BLUE}Outputting for Switch")
        hk.to_switch()
    else:
        print(f"{Fore.BLUE}Outputting for Wii U")
        hk.to_wiiu()

    Messages.serializing(outFile)
    hk.serialize()

    Messages.writing(outFile)
    hk.to_file(outFile)


def main():
    init(autoreset=True)

    args = parse_args()

    json_to_hk(args.jsonFile, args.outFile, args.switch)

    Messages.done()


if __name__ == "__main__":
    main()
