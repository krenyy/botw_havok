import argparse

from .. import Havok
from .common import Messages, change_extension, check_if_exists, init


def parse_args():
    parser = argparse.ArgumentParser(description="Convert Havok packfile to JSON")
    parser.add_argument("hkFile", help="Path to a Havok packfile")
    parser.add_argument("outFile", help="Path to destination JSON file", nargs="?")

    return parser.parse_args()


def hk_to_json(hkFile: str, outFile: str):
    if not outFile:
        outFile = change_extension(hkFile, "json")
        check_if_exists(outFile)

    Messages.loading(hkFile)
    hk = Havok.from_file(hkFile)

    Messages.deserializing(hkFile)
    hk.deserialize()

    Messages.writing(outFile)
    hk.to_json(outFile, pretty_print=True)


def main():
    init()

    args = parse_args()

    hk_to_json(args.hkFile, args.outFile)

    Messages.done()


if __name__ == "__main__":
    main()
