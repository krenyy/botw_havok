import argparse
import json
import os
from copy import deepcopy

from .. import Havok

templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")


def main():
    parser = argparse.ArgumentParser(
        description="Convert Havok Static Compound (.hksc) to Havok Rigid Body array (.hkrb)"
    )
    parser.add_argument("hkscFile", help="Path to a Havok Static Compound file")
    parser.add_argument(
        "outFile", help="Path to the destination Havok Rigid Body file", nargs="?"
    )

    args = parser.parse_args()

    hk = Havok.from_file(args.hkscFile)
    hk.deserialize()

    nx = hk.files[0].header.pointer_size == 8

    shapes = []  # Final shapes to be converted to hkrb

    for rigidbody in (
        hk.files[1].data.contents[0].namedVariants[0].variant.systems[0].rigidBodies
    ):
        for instance in rigidbody.collidable.shape.instances:
            shapes.append(instance.shape)

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
