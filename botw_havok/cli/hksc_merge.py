import argparse
import datetime
from copy import deepcopy
from typing import List

from botw_havok.classes.common.ActorInfo import ActorInfo

from botw_havok.classes.common.ShapeInfo import ShapeInfo

from botw_havok.binary.types import UInt32
from colorama import init

from .common import Messages, Path, Templates, check_if_exists
from .. import Havok


def parse_args():
    parser = argparse.ArgumentParser(
        description="Merge two Havok Static Compound (.hksc) files"
    )
    parser.add_argument(
        "hkscFile", type=Path, help="Path to a Havok Static Compound file"
    )
    parser.add_argument(
        "hkscFile1", type=Path, help="Path to Havok Static Compound file"
    )
    parser.add_argument(
        "--hashid", type=UInt32, help="HashId used for added shapes", nargs="?"
    )
    parser.add_argument(
        "-nx", "--switch", action="store_true", help="Use to output the file for Switch"
    )
    parser.add_argument(
        "outFile",
        type=Path,
        help="Path to the destination Havok Static Compound file",
        nargs="?",
    )

    return parser.parse_args()


def main():
    init(autoreset=True)

    args = parse_args()

    Messages.loading(args.hkscFile)
    hk = Havok.from_file(args.hkscFile)

    Messages.deserializing(args.hkscFile)
    hk.deserialize()

    Messages.loading(args.hkscFile1)
    hk1 = Havok.from_file(args.hkscFile1)

    Messages.deserializing(args.hkscFile1)
    hk1.deserialize()

    HashId = (
        args.hashid
        if args.hashid
        else max([ai.HashId for ai in hk.files[0].data.contents[0].ActorInfo]) + 1
    )

    if (
        HashId in [ai.HashId for ai in hk.files[0].data.contents[0].ActorInfo]
        or HashId > 0xFFFFFFFF
    ):
        raise SystemExit("HashId already used or not valid!")

    shapenum = len(hk1.files[0].data.contents[0].ShapeInfo)

    ai = ActorInfo()
    ai.HashId = HashId
    ai.SRTHash = 0  # TODO: Investigate further
    ai.ShapeInfoStart = len(hk.files[0].data.contents[0].ShapeInfo)
    ai.ShapeInfoEnd = ai.ShapeInfoStart + shapenum

    hk.files[0].data.contents[0].ActorInfo.append(ai)

    shape_index = ai.ShapeInfoStart

    rbs = []

    for shape in [
        rb.collidable.shape
        for rb in hk1.files[1]
        .data.contents[0]
        .namedVariants[0]
        .variant.systems[0]
        .rigidBodies
    ]:
        rb = deepcopy(Templates.hkpRigidBody)
        rb["name"] = str(datetime.datetime.now())

        for i, inst in enumerate(shape.instances):
            si = ShapeInfo()
            si.ActorInfoIndex = len(hk.files[0].data.contents[0].ActorInfo) - 1
            si.InstanceId = ai.ShapeInfoStart + shape_index  # ?
            si.BodyGroup = 0  # Seems to be 0 or 5, no idea what it does
            si.BodyLayerType = 0

            hk.files[0].data.contents[0].ShapeInfo.append(si)

            shape.instances[i].userData = shape_index
            shape_index += 1

        rb["collidable"]["shape"] = shape.as_dict()

        rbs.append(rb)

    hk = hk.as_dict()
    hk[1]["data"]["contents"][0]["namedVariants"][0]["variant"]["systems"][0][
        "rigidBodies"
    ].extend(rbs)

    outFile = (
        args.outFile
        if args.outFile
        else args.hkscFile.with_name("Merged").with_suffix(".hksc")
    )
    check_if_exists(outFile)

    hk = Havok.from_dict(hk, outFile)

    if args.switch:
        hk.to_switch()
    else:
        hk.to_wiiu()

    Messages.serializing(outFile)
    hk.serialize()

    Messages.writing(outFile)
    hk.to_file(outFile)


if __name__ == "__main__":
    main()
