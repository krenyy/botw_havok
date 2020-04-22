import argparse

from colorama import Fore, init

from .. import Havok
from .common import Messages, change_extension, check_if_exists


def main():
    init(autoreset=True, convert=True)

    parser = argparse.ArgumentParser(description="Convert Havok packfile to JSON")
    parser.add_argument("hkFile", help="Path to a Havok packfile")
    parser.add_argument("outFile", help="Path to destination JSON file", nargs="?")
    parser.add_argument(
        "-p", "--pretty-print", action="store_true", help="Pretty-print the JSON"
    )
    args = parser.parse_args()

    if not args.outFile:
        args.outFile = change_extension(args.hkFile, "json")

        check_if_exists(args.outFile)

    Messages.loading(args.hkFile)
    hk = Havok.from_file(args.hkFile)

    print(f"{Fore.BLUE}Deserializing")
    hk.deserialize()

    Messages.writing(args.outFile)
    hk.to_json(args.outFile, args.pretty_print)

    Messages.done()


if __name__ == "__main__":
    main()
