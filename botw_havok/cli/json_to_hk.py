from .. import Havok
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Convert a valid JSON file to a Havok packfile"
    )
    parser.add_argument(
        "--nx", action="store_true", help="Convert to Nintendo Switch packfile"
    )
    parser.add_argument("jsonFile", help="Path to a JSON file")
    parser.add_argument("-o", "--out", help="Path to destination Havok packfile")
    args = parser.parse_args()

    hk = Havok.from_json(args.jsonFile)

    if args.out:
        hkFile = args.out
    else:
        hkFile = ".".join(args.jsonFile.split(".")[:-1]) + ".hkx"

    if args.nx:
        hk.to_switch()
    else:
        hk.to_wiiu()

    hk.to_file(hkFile)


if __name__ == "__main__":
    main()
