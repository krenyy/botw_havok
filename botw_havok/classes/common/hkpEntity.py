from .hkpWorldObject import hkpWorldObject
from .hkpMaterial import hkpMaterial
from ...binary import BinaryReader, BinaryWriter

if False:
    from ...hk import HK
    from ...container.sections.hkobject import HKObject


class hkpEntity(hkpWorldObject):
    material: hkpMaterial
    limitContactImpulseUtilAndFlag: None = None
    damageMultiplier: float
    breakableBody: None = None
    solverData: int
    storageIndex: int
    contactPointCallbackDelay: int

    def deserialize(self, hk: "HK", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hk, br, obj)

        self.material = hkpMaterial()
        self.material.deserialize(hk, br)

        if hk.header.padding_option:
            br.align_to(16)

        limitContactImpulseUtilAndFlag_offset = br.tell()
        hk._assert_pointer(br)  # limitContactImpulseUtilAndFlag

        self.damageMultiplier = br.read_single()

        if hk.header.padding_option:
            br.align_to(16)

        breakableBody_offset = br.tell()
        hk._assert_pointer(br)  # breakableBody

        
