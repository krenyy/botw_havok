from pathlib import Path

from .. import Havok

hk_path = Path("/home/kreny/Desktop/hkfilesfordump")
signature_path = Path("/home/kreny/Desktop/hk_signature_map.py")

string = "hk_signature_map = "
signature_map = {}

for file in hk_path.iterdir():
    hk = Havok()
    hk.read(file)
    for hkfile in hk.files:
        for hkcls in hkfile.classnames.classes:
            signature_map.update({hkcls.name: hkcls.signature})

with open(signature_path, "w") as f:
    f.write(string + str(signature_map))
