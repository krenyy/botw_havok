import argparse

from colorama import init

from .common import Fore, Messages, Path
from .. import Havok


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compare Havok packfiles.\nAlso works between Wii U and Switch packfiles."
    )
    parser.add_argument(
        "hkFiles", type=Path, help="Paths to Havok packfiles for comparison", nargs="+"
    )

    return parser.parse_args()


def main():
    init(autoreset=True)

    args = parse_args()

    if not args.hkFiles or len(args.hkFiles) <= 1:
        return None

    files = []
    for hkFile in args.hkFiles:
        Messages.loading(hkFile)
        hk = Havok.from_file(hkFile)

        Messages.deserializing(hkFile)
        hk.deserialize()

        files.append(hk)

    for i in range(len(files) - 1):
        print(
            f"{Fore.BLUE}Comparing '{files[i].path.name}' and '{files[i + 1].path.name}'"
        )
        for hkfile0, hkfile1 in zip(files[i].files, files[i + 1].files):
            if hkfile0.data.contents[0] == hkfile1.data.contents[0]:
                print(f"{Fore.GREEN}File contents match!")
            else:
                print(f"{Fore.RED}File contents do not match!")

    Messages.done()


if __name__ == "__main__":
    main()
