from .. import Havok
import argparse


def main():
    parser = argparse.ArgumentParser(description="Convert Havok packfile to JSON")
    parser.add_argument("hkFile", help="Path to a Havok packfile")
    parser.add_argument("jsonFile", help="Path to destination JSON file")
    args = parser.parse_args()

    hk = Havok.from_file(args.hkFile)
    hk.to_json(args.jsonFile)


if __name__ == "__main__":
    main()
