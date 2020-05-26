import argparse

from colorama import init

from .common import Fore, Messages, Path, check_if_exists
from .. import Havok


def parse_args():
    parser = argparse.ArgumentParser(description="Convert Havok JSON file to packfile")
    parser.add_argument("jsonFile", type=Path, help="Path to destination JSON file")
    parser.add_argument(
        "outFile", type=Path, help="Path to a Havok packfile", nargs="?"
    )
    parser.add_argument(
        "-nx", "--switch", action="store_true", help="Use to output the file for Switch"
    )

    return parser.parse_args()


def json_to_hk(jsonFile: Path, outFile: Path, nx: bool):
    Messages.loading(jsonFile)
    hk = Havok.from_json(jsonFile)

    if not outFile:
        outFile = jsonFile.with_suffix(hk.guess_extension())
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
