import argparse

from .. import Havok
from .common import Messages, change_extension, check_if_exists, init


def parse_args():
    parser = argparse.ArgumentParser(description="Convert Havok packfile to JSON")
    parser.add_argument("hkFile", help="Path to a Havok packfile")
    parser.add_argument("outFile", help="Path to destination JSON file", nargs="?")
    parser.add_argument(
        "-p", "--pretty-print", help="Pretty-print the JSON file", action="store_true"
    )

    return parser.parse_args()


def hk_to_json(hkFile: str, outFile: str, pretty_print: bool):
    if not outFile:
        outFile = change_extension(hkFile, "json")
        check_if_exists(outFile)

    Messages.loading(hkFile)
    hk = Havok.from_file(hkFile)

    Messages.deserializing(hkFile)
    hk.deserialize()

    Messages.writing(outFile)
    hk.to_json(outFile, pretty_print=pretty_print)


def main():
    init(autoreset=True)

    args = parse_args()

    hk_to_json(args.hkFile, args.outFile, args.pretty_print)

    Messages.done()


if __name__ == "__main__":
    main()
