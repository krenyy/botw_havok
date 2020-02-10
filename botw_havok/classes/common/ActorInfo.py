from ...binary import BinaryReader, BinaryWriter


class ActorInfo:
    HashId: int
    SRTHash: int
    ShapeInfoStart: int
    ShapeInfoEnd: int

    def __init__(self, d: dict = None):
        if d:
            (
                self.HashId,
                self.SRTHash,
                self.ShapeInfoStart,
                self.ShapeInfoEnd,
            ) = d.values()

    def read(self, br: BinaryReader):
        self.HashId = br.read_uint32()
        self.SRTHash = br.read_int32()
        self.ShapeInfoStart = br.read_int32()
        self.ShapeInfoEnd = br.read_int32()

    def write(self, bw: BinaryWriter):
        bw.write_uint32(self.HashId)
        bw.write_int32(self.SRTHash)
        bw.write_int32(self.ShapeInfoStart)
        bw.write_int32(self.ShapeInfoEnd)

    def asdict(self):
        return {
            "HashId": self.HashId,
            "SRTHash": self.SRTHash,
            "ShapeInfoStart": self.ShapeInfoStart,
            "ShapeInfoEnd": self.ShapeInfoEnd,
        }

    @classmethod
    def fromdict(cls, d: dict):
        return cls(d)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.HashId}, "
            f"{self.SRTHash}, {self.ShapeInfoStart}, "
            f"{self.ShapeInfoEnd})"
        )
