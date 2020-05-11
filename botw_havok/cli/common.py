import os
from copy import deepcopy
import json
from colorama import Fore, init

from .. import Havok

templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")


class Templates:
    hkrb: list = json.load(open(os.path.join(templates_dir, "hkrb.json"), "r"))
    hkpRigidBody: dict = json.load(
        open(os.path.join(templates_dir, "hkpRigidBody.json"), "r")
    )

    bphysics: str = open(os.path.join(templates_dir, "bphysics.yml"), "r").read()
    bphysics_rigidbody: str = open(
        os.path.join(templates_dir, "bphysics_rigidbody.yml"), "r"
    ).read()


class Messages:
    ext_descriptions: dict = {
        "hksc": "Static Compound",
        "hkrb": "Rigid Body",
        "hktmrb": "TeraMesh",
        "hknm2": "NavMesh",
        "hkcl": "Cloth",
        "hkrg": "Ragdoll",
        "hkx": "Unknown",
    }

    @staticmethod
    def loading(file: str):
        print(f"{Fore.BLUE}Loading '{os.path.basename(file)}' to memory")

    @staticmethod
    def writing(file: str):
        print(f"{Fore.BLUE}Writing '{os.path.basename(file)}'")

    @staticmethod
    def serializing(file: str):
        print(f"{Fore.BLUE}Serializing '{os.path.basename(file)}'")

    @staticmethod
    def deserializing(file: str):
        print(f"{Fore.BLUE}Deserializing '{os.path.basename(file)}'")

    @classmethod
    def check_type(cls, file: Havok, extension: str):
        ext = file.guess_extension()

        if ext != extension:
            raise SystemExit(
                f"{Fore.RED}This is a {cls.ext_descriptions[ext]} file! You need a {cls.ext_descriptions[extension]} file!"
            )

    @staticmethod
    def done():
        print(f"{Fore.GREEN}Done!")


def shapes_to_hkrb(shapes: list, hkscFile: str, outFile: str, nx: bool):
    if not shapes:
        raise SystemExit("For some reason, no shapes were found.")

    if not outFile:
        outFile = change_extension(hkscFile, "hkrb")

        check_if_exists(outFile)

    hkrb_template = deepcopy(Templates.hkrb)
    bphysics_rigidbodies = []
    for i, shape in enumerate(shapes):
        hk_rb = deepcopy(Templates.hkpRigidBody)
        bp_rb = Templates.bphysics_rigidbody

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

    Messages.serializing(outFile)
    hkrb.serialize()

    Messages.writing(outFile)
    hkrb.to_file(outFile)

    with open(change_extension(outFile, "yml"), "w") as f:
        f.write(
            Templates.bphysics.format(
                len(bphysics_rigidbodies), "\n".join(bphysics_rigidbodies)
            )
        )


def check_if_exists(file: str):
    if os.path.isfile(file):
        choice = input(
            f"{Fore.YELLOW}'{os.path.basename(file)}' exists, do you wish to overwrite it?\n$ "
        ).upper()
        if choice.startswith("Y"):
            pass
        else:
            raise SystemExit(f"{Fore.RED}Operation aborted!")


def change_extension(file: str, extension: str) -> str:
    return f'{".".join(file.split(".")[:-1])}.{extension}'
