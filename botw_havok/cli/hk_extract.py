import argparse
import json
import os
from copy import deepcopy

from .. import Havok

templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")


def main():
    parser = argparse.ArgumentParser(
        description="Extract HKRB actor collision from a single HKSC compound file"
    )
    parser.add_argument("hkscFile", help="Path to a Havok StaticCompound file")
    parser.add_argument("hashId", type=int, help="HashId to extract")
    parser.add_argument(
        "outFile", help="Path to the destination Havok RigidBody file", nargs="?"
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Extract all shapes matching the provided HashId (should be used only if it doesn't work without it)",
    )
    args = parser.parse_args()

    hk = Havok.from_file(args.hkscFile)
    hk.deserialize()

    nx = hk.files[0].header.pointer_size == 8

    try:
        ai = [
            ai
            for ai in hk.files[0].data.contents[0].ActorInfo
            if ai.HashId == args.hashId
        ][0]
    except IndexError:
        raise Exception(
            f"HashId '{args.hashId}' doesn't exist in this StaticCompound file!"
        )

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

                if not args.all:
                    break

    if not shapes:
        raise Exception("For some reason, no shapes were found.")

    if not args.outFile:
        args.outFile = ".".join(args.hkscFile.split(".")[:-1] + ["hkrb"])

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
        hk_rb["collidable"]["shape"] = shape.asdict()

        hkrb_template[0]["data"]["contents"][0]["namedVariants"][0]["variant"][
            "systems"
        ][0]["rigidBodies"].append(hk_rb)

        bphysics_rigidbodies.append(bp_rb.format(i))

    hkrb = Havok.fromdict(hkrb_template)

    if nx:
        hkrb.to_switch()
    else:
        hkrb.to_wiiu()

    hkrb.serialize()
    hkrb.to_file(args.outFile)

    with open(".".join(args.outFile.split(".")[:-1] + ["yml"]), "w") as f:
        f.write(
            bphysics_template.format(
                len(bphysics_rigidbodies), "\n".join(bphysics_rigidbodies)
            )
        )


if __name__ == "__main__":
    main()
