import argparse

from colorama import init

from .common import Messages, Path, check_if_exists
from .. import Havok


def parse_args():
    parser = argparse.ArgumentParser(description="Convert Havok packfile to JSON")
    parser.add_argument("hkFile", type=Path, help="Path to a Havok packfile")
    parser.add_argument(
        "outFile", type=Path, help="Path to destination JSON file", nargs="?"
    )
    parser.add_argument(
        "-p", "--pretty-print", help="Pretty-print the JSON file", action="store_true"
    )

    return parser.parse_args()


def hk_to_json(hkFile: Path, outFile: Path, pretty_print: bool):
    if not outFile:
        outFile = hkFile.with_suffix(".json")
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
