import argparse

from .. import Havok
from .common import Fore, Messages, change_extension, check_if_exists, init


def parse_args():
    parser = argparse.ArgumentParser(description="Convert Havok packfile to JSON")
    parser.add_argument("hkFile", help="Path to a Havok packfile")
    parser.add_argument("outFile", help="Path to destination JSON file", nargs="?")
    parser.add_argument(
        "-nx", "--switch", action="store_true", help="Use to output the file for Switch"
    )

    return parser.parse_args()


def hk_to_json(data: bytes, hkFile: str, outFile: str):
    if not outFile:
        outFile = change_extension(hkFile, "json")
        check_if_exists(outFile)

    Messages.loading(hkFile)
    hk = Havok.from_file(hkFile)

    Messages.deserializing(hkFile)
    hk.deserialize()

    Messages.writing(outFile)
    hk.to_json(outFile, pretty_print=True)


def json_to_hk(data: bytes, jsonFile: str, outFile: str, nx: bool):
    Messages.loading(jsonFile)
    hk = Havok.from_json(jsonFile)

    if not outFile:
        outFile = change_extension(jsonFile, hk.guess_extension())

        check_if_exists(outFile)

    if nx:
        print(f"{Fore.BLUE}'--nx' flag set, outputting as Switch")
        hk.to_switch()
    else:
        print(f"{Fore.BLUE}'--nx' flag not set, outputting as Wii U")
        hk.to_wiiu()

    Messages.writing(outFile)
    hk.to_file(outFile)


def main():
    init()

    args = parse_args()

    with open(args.hkFile, "rb") as f:
        data = f.read()

    if data[0:4] != b"\x57\xE0\xE0\x57" and data[0:4] != b"Yaz0":
        json_to_hk(data, args.hkFile, args.outFile, args.switch)
    else:
        hk_to_json(data, args.hkFile, args.outFile)

    Messages.done()


if __name__ == "__main__":
    main()
