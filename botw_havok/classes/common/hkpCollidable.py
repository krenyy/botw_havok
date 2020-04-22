from ...binary import BinaryReader, BinaryWriter
from ...binary.types import Float32, Int8, UInt8, UInt16
from ..enums.ForceCollideOntoPpuReasons import ForceCollideOntoPpuReasons
from .hkpCdBody import hkpCdBody
from .hkpCollidableBoundingVolumeData import hkpCollidableBoundingVolumeData
from .hkpTypedBroadPhaseHandle import hkpTypedBroadPhaseHandle

if False:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpCollidable(hkpCdBody):
    ownerOffset: Int8
    forceCollideOntoPpu: UInt8
    shapeSizeOnSpu: UInt16
    broadPhaseHandle: hkpTypedBroadPhaseHandle
    boundingVolumeData: hkpCollidableBoundingVolumeData
    allowedPenetrationDepth: Float32

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        self.ownerOffset = br.read_int8()
        self.forceCollideOntoPpu = br.read_uint8()
        self.shapeSizeOnSpu = br.read_uint16()

        self.broadPhaseHandle = hkpTypedBroadPhaseHandle()
        self.broadPhaseHandle.deserialize(hkFile, br, obj)

        self.boundingVolumeData = hkpCollidableBoundingVolumeData()
        self.boundingVolumeData.deserialize(hkFile, br, obj)

        self.allowedPenetrationDepth = br.read_float32()
        br.align_to(16)  # Padding

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        bw.write_int8(self.ownerOffset)
        bw.write_uint8(self.forceCollideOntoPpu)
        bw.write_uint16(self.shapeSizeOnSpu)

        self.broadPhaseHandle.serialize(hkFile, bw, obj)

        self.boundingVolumeData.serialize(hkFile, bw, obj)

        bw.write_float32(self.allowedPenetrationDepth)
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
