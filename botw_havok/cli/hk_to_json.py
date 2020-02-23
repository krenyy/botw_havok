from .. import Havok
import argparse


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
        jsonFile = ".".join(args.hkFile.split(".")[:-1]) + ".json"

    hk = Havok.from_file(args.hkFile)
    hk.to_json(jsonFile, args.pretty_print)


if __name__ == "__main__":
    main()
