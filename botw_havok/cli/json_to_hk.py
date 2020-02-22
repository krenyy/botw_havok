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
    parser.add_argument("hkFile", help="Path to destination Havok packfile")
    args = parser.parse_args()

    hk = Havok.from_file(args.hkFile)
    hk.to_json(args.jsonFile)


if __name__ == "__main__":
    main()
