from ...binary import BinaryReader, BinaryWriter

if False:
    from ...hk import HK


class hkMultiThreadCheck:
    threadId: int
    stackTraceId: int
    markCount: int
    markBitStack: int

    def deserialize(self, hk: "HK", br: BinaryReader):
        self.threadId = br.read_uint32()
        self.stackTraceId = br.read_uint32()
        self.markCount = br.read_uint16()
        self.markBitStack = br.read_uint16()

    def serialize(self, hk: "HK", bw: BinaryWriter):
        bw.write_uint32(self.threadId)
        bw.write_uint32(self.stackTraceId)
        bw.write_uint16(self.markCount)
        bw.write_uint16(self.markBitStack)

    def asdict(self):
        return {
            "threadId": self.threadId,
            "stackTraceId": self.stackTraceId,
            "markCount": self.markCount,
            "markBitStack": self.markBitStack,
        }

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.threadId = d["threadId"]
        inst.stackTraceId = d["stackTraceId"]
        inst.markCount = d["markCount"]
        inst.markBitStack = d["markBitStack"]

        return inst
