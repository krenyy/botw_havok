import argparse
import json
import os
from copy import deepcopy
from typing import List

from .. import Havok
from ..binary.types import UInt32
from ..classes.common.ActorInfo import ActorInfo
from .common import Messages, change_extension, check_if_exists, templates_dir


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract HKRB actor collision from a single HKSC compound file"
    )
    parser.add_argument("hkscFile", help="Path to a Havok StaticCompound file")
    parser.add_argument("hashId", type=UInt32, help="HashId to extract")
    parser.add_argument(
        "outFile", help="Path to the destination Havok RigidBody file", nargs="?"
    )

    return parser.parse_args()


def binary_search(l: List[ActorInfo], hashId: UInt32):
    first = 0
    last = len(l) - 1

    while first <= last:
        mid = (first + last) // 2
        if l[mid].HashId == hashId:
            return l[mid]
        else:
            if hashId > l[mid].HashId:
                first = mid + 1
            else:
                last = mid - 1

    raise SystemExit(f"HashId '{hashId}' doesn't exist in this StaticCompound file!")


def main():
    args = parse_args()

    Messages.loading(args.hkscFile)
    hk = Havok.from_file(args.hkscFile)

    Messages.deserializing(args.hkscFile)
    hk.deserialize()

    nx = hk.files[0].header.pointer_size == 8

    ai = binary_search(hk.files[0].data.contents[0].ActorInfo, args.hashId)

    shapes = []  # Final shapes to be converted to hkrb

    shapeinfo_range = range(ai.ShapeInfoStart, ai.ShapeInfoEnd + 1)

    for rigidbody in (
        hk.files[1].data.contents[0].namedVariants[0].variant.systems[0].rigidBodies
    ):
        for instance in rigidbody.collidable.shape.instances:
            if (
                instance.userData in shapeinfo_range
            ):  # Nintendo stores ShapeInfo index inside 'userData' key
                shapes.append(instance.shape)

    if not shapes:
        raise SystemExit("For some reason, no shapes were found.")

    if not args.outFile:
        args.outFile = change_extension(args.hkscFile, "hkrb")

        check_if_exists(args.outFile)

    yml_file = change_extension(args.outFile, "yml")
    check_if_exists(yml_file)

    with open(os.path.join(templates_dir, "hkrb.json"), "r") as f:
        hkrb_template = json.load(f)

    with open(os.path.join(templates_dir, "hkrb_rigidbody.json"), "r") as f:
        hk_rigidbody_template = json.load(f)

    with open(os.path.join(templates_dir, "bphysics.yml"), "r") as f:
        bphysics_template = f.read()

    with open(os.path.join(templates_dir, "bphysics_rigidbody.yml"), "r") as f:
        bphysics_rigidbody_template = f.read()

    bphysics_rigidbodies = []
    for i, shape in enumerate(shapes):
        hk_rb = deepcopy(hk_rigidbody_template)
        bp_rb = bphysics_rigidbody_template

        hk_rb["name"] = f"Shape_{i}"
        hk_rb["collidable"]["shape"] = shape.as_dict()

        hkrb_template[0]["data"]["contents"][0]["namedVariants"][0]["variant"][
            "systems"
        ][0]["rigidBodies"].append(hk_rb)

        bphysics_rigidbodies.append(bp_rb.format(i))

    hkrb = Havok.from_dict(hkrb_template)

    if nx:
        hkrb.to_switch()
    else:
        hkrb.to_wiiu()

    Messages.serializing(args.outFile)
    hkrb.serialize()

    Messages.writing(args.outFile)
    hkrb.to_file(args.outFile)

    with open(yml_file, "w") as f:
        f.write(
            bphysics_template.format(
                len(bphysics_rigidbodies), "\n".join(bphysics_rigidbodies)
            )
        )


if __name__ == "__main__":
    main()
