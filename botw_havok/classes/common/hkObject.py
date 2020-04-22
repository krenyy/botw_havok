from ...binary import BinaryReader, BinaryWriter

if False:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkObject:
    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        raise NotImplementedError("This method is meant to be overridden!")

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        raise NotImplementedError("This method is meant to be overridden!")
