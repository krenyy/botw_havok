import argparse

from .. import Havok
import botw_havok.cli.util as cliutil


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

    if args.out:
        hkFile = args.out
    else:
        hkFile = cliutil.change_extension(args.jsonFile, "hkx")

        cliutil.check_if_exists(hkFile)

    cliutil.Messages.loading(args.jsonFile)
    hk = Havok.from_json(args.jsonFile)

    if args.nx:
        print(f"{cliutil.Fore.BLUE}--nx flag set, outputting as Switch")
        hk.to_switch()
    else:
        print(f"{cliutil.Fore.BLUE}--nx flag not set, outputting as Wii U")
        hk.to_wiiu()

    cliutil.Messages.writing(hkFile)
    hk.to_file(hkFile)

    cliutil.Messages.done()


if __name__ == "__main__":
    main()
