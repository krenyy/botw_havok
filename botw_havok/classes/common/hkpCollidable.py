from .hkpCdBody import hkpCdBody
from ...binary import BinaryReader, BinaryWriter
from .hkpTypedBroadPhaseHandle import hkpTypedBroadPhaseHandle
from .hkpCollidableBoundingVolumeData import hkpCollidableBoundingVolumeData
from ..enums.ForceCollideOntoPpuReasons import ForceCollideOntoPpuReasons

if False:
    from ...hk import HK


class hkpCollidable(hkpCdBody):
    ownerOffset: int
    forceCollideOntoPpu: int
    shapeSizeOnSpu: int
    broadPhaseHandle: hkpTypedBroadPhaseHandle
    boundingVolumeData: hkpCollidableBoundingVolumeData
    allowedPenetrationDepth: float

    def deserialize(self, hk: "HK", br: BinaryReader, obj):
        super().deserialize(hk, br, obj)

        self.ownerOffset = br.read_int8()
        self.forceCollideOntoPpu = br.read_uint8()
        self.shapeSizeOnSpu = br.read_uint16()

        self.broadPhaseHandle = hkpTypedBroadPhaseHandle()
        self.broadPhaseHandle.deserialize(hk, br)

        self.boundingVolumeData = hkpCollidableBoundingVolumeData()
        self.boundingVolumeData.deserialize(hk, br)

        self.allowedPenetrationDepth = br.read_single()
        br.align_to(16)  # Padding

    def serialize(self, hk: "HK", bw: BinaryWriter, obj):
        super().serialize(hk, bw, obj)

        bw.write_int8(self.ownerOffset)
        bw.write_uint8(self.forceCollideOntoPpu)
        bw.write_uint16(self.shapeSizeOnSpu)

        self.broadPhaseHandle.serialize(hk, bw)

        self.boundingVolumeData.serialize(hk, bw)

        bw.write_single(self.allowedPenetrationDepth)
        bw.align_to(16)

    def asdict(self):
        d = super().asdict()
        d.update(
            {
                "ownerOffset": self.ownerOffset,
                "forceCollideOntoPpu": ForceCollideOntoPpuReasons(
                    self.forceCollideOntoPpu
                ).name,
                "shapeSizeOnSpu": self.shapeSizeOnSpu,
                "broadPhaseHandle": self.broadPhaseHandle.asdict(),
                "boundingVolumeData": self.boundingVolumeData.asdict(),
                "allowedPenetrationDepth": self.allowedPenetrationDepth,
            }
        )
        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.__dict__.update(super().fromdict(d).__dict__)

        inst.ownerOffset = d["ownerOffset"]
        inst.forceCollideOntoPpu = getattr(
            ForceCollideOntoPpuReasons, d["forceCollideOntoPpu"]
        ).value
        inst.shapeSizeOnSpu = d["shapeSizeOnSpu"]
        inst.broadPhaseHandle = hkpTypedBroadPhaseHandle.fromdict(d["broadPhaseHandle"])
        inst.boundingVolumeData = hkpCollidableBoundingVolumeData.fromdict(
            d["boundingVolumeData"]
        )
        inst.allowedPenetrationDepth = d["allowedPenetrationDepth"]

        return inst
