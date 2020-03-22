import argparse

from .. import Havok
from .util import Messages, change_extension, check_if_exists, Fore


def main():
    parser = argparse.ArgumentParser(description="Convert Havok packfile to JSON")
    parser.add_argument("hkFile", help="Path to a Havok packfile")
    parser.add_argument("-o", "--out", help="Path to destination JSON file")
    parser.add_argument(
        "-p", "--pretty-print", action="store_true", help="Pretty-print the JSON"
    )
    args = parser.parse_args()

    if args.out:
        jsonFile = args.out
    else:
        jsonFile = change_extension(args.hkFile, "json")

        check_if_exists(jsonFile)

    Messages.loading(args.hkFile)
    hk = Havok.from_file(args.hkFile)

    print(f"{Fore.BLUE}Deserializing")
    hk.deserialize()

    Messages.writing(jsonFile)
    hk.to_json(jsonFile, args.pretty_print)

    Messages.done()


if __name__ == "__main__":
    main()
