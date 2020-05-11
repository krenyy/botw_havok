import argparse

from .. import Havok
from .common import Fore, Messages, change_extension, check_if_exists, init


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compare Havok packfiles.\nAlso works between Wii U and Switch packfiles."
    )
    parser.add_argument(
        "hkFiles", help="Paths to Havok packfiles for comparison", nargs="+"
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

    print(f"{Fore.BLUE}Comparing")
    for i in range(len(files) - 1):
        for file0, file1 in zip(files[i].files, files[i + 1].files):
            if file0.data.contents[0] != file1.data.contents[0]:
                print(f"{Fore.RED}File contents don't match")
                break
        else:
            print(f"{Fore.GREEN}File contents match")

    Messages.done()


if __name__ == "__main__":
    main()
