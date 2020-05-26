import json
from copy import deepcopy
from pathlib import Path

from colorama import Fore

from .. import Havok

templates_dir = Path(__file__).parent.absolute().resolve() / "templates"


class Templates:
    hkrb: list = json.load(Path(templates_dir / "hkrb.json").open("r"))
    hkpRigidBody: dict = json.load(Path(templates_dir / "hkpRigidBody.json").open("r"))
    bphysics: str = Path(templates_dir, "bphysics.yml").read_text()
    bphysics_rigidbody: str = Path(templates_dir, "bphysics_rigidbody.yml").read_text()


class Messages:
    ext_descriptions: dict = {
        ".hksc": "Static Compound",
        ".hkrb": "Rigid Body",
        ".hktmrb": "TeraMesh",
        ".hknm2": "NavMesh",
        ".hkcl": "Cloth",
        ".hkrg": "Ragdoll",
        ".hkx": "Unknown",
    }

    @staticmethod
    def loading(file: Path):
        print(f"{Fore.BLUE}Loading '{file.name}' to memory")

    @staticmethod
    def writing(file: Path):
        print(f"{Fore.BLUE}Writing '{file.name}'")

    @staticmethod
    def serializing(file: Path):
        print(f"{Fore.BLUE}Serializing '{file.name}'")

    @staticmethod
    def deserializing(file: Path):
        print(f"{Fore.BLUE}Deserializing '{file.name}'")

    @classmethod
    def check_type(cls, file: Havok, extension: str):
        ext = file.guess_extension()

        if ext != extension:
            raise SystemExit(
                f"{Fore.RED}This is a {cls.ext_descriptions[ext]} file! You need a {cls.ext_descriptions[extension]} ({extension}) file!"
            )

    @staticmethod
    def done():
        print(f"\n{Fore.GREEN}Done!\n")


def shapes_to_hkrb(shapes: list, hkscFile: Path, outFile: Path, nx: bool):
    if not shapes:
        raise SystemExit("For some reason, no shapes were found.")

    if not outFile:
        outFile = hkscFile.with_suffix(".hkrb")

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

    outFile.with_suffix(".yml").write_text(
        Templates.bphysics.format(
            len(bphysics_rigidbodies), "\n".join(bphysics_rigidbodies)
        )
    )


def check_if_exists(file: Path):
    if file.exists() and file.is_file():
        choice = input(
            f"{Fore.YELLOW}'{file.name}' exists, do you wish to overwrite it?\n$ "
        ).upper()
        if choice.startswith("Y"):
            pass
        else:
            raise SystemExit(f"{Fore.RED}Operation aborted!")
