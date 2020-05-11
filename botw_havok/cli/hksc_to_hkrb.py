import argparse
import json
import os
from copy import deepcopy

from .. import Havok
from .common import Messages, init, shapes_to_hkrb


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert Havok Static Compound (.hksc) to Havok Rigid Body array (.hkrb)"
    )
    parser.add_argument("hkscFile", help="Path to a Havok Static Compound file")
    parser.add_argument(
        "outFile", help="Path to the destination Havok Rigid Body file", nargs="?"
    )

    return parser.parse_args()


def main():
    init(autoreset=True)

    args = parse_args()

    Messages.loading(args.hkscFile)
    hk = Havok.from_file(args.hkscFile)

    Messages.deserializing(args.hkscFile)
    hk.deserialize()

    nx = hk.files[0].header.pointer_size == 8

    shapes = [
        instance.shape
        for rigidbody in hk.files[1]
        .data.contents[0]
        .namedVariants[0]
        .variant.systems[0]
        .rigidBodies
        for instance in rigidbody.collidable.shape.instance
    ]

    shapes_to_hkrb(shapes, args.hkscFile, args.outFile, nx)


if __name__ == "__main__":
    main()
