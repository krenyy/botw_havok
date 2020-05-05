import argparse

from colorama import Fore, init

from .. import Havok
from .common import Messages, change_extension, check_if_exists


def main():
    init(autoreset=True, convert=True)

    parser = argparse.ArgumentParser(
        description="Convert a valid JSON file to a Havok packfile"
    )
    parser.add_argument("jsonFile", help="Path to a JSON file")
    parser.add_argument("outFile", help="Path to destination Havok packfile", nargs="?")
    parser.add_argument(
        "--nx", action="store_true", help="Convert to Nintendo Switch packfile"
    )
    args = parser.parse_args()

    if not args.outFile:
        args.outFile = change_extension(args.jsonFile, "hkx")

        check_if_exists(args.outFile)

    Messages.loading(args.jsonFile)
    hk = Havok.from_json(args.jsonFile)

    if args.nx:
        print(f"{Fore.BLUE}'--nx' flag set, outputting as Switch")
        hk.to_switch()
    else:
        print(f"{Fore.BLUE}'--nx' flag not set, outputting as Wii U")
        hk.to_wiiu()

    Messages.writing(args.outFile)
    hk.to_file(args.outFile)

    Messages.done()


if __name__ == "__main__":
    main()
