from ..binary import BinaryReader, BinaryWriter
from ..binary.types import Int8, Int16, Int32, UInt8, UInt16, UInt32


class HKHeader:
    """Represents Havok file header
    """

    # fmt:off
    magic0: UInt32 = 0x57E0E057  # 0x00  # Always 0x57E0E057
    magic1: UInt32 = 0x10C0C010  # 0x04  # Always 0x10C0C010
    user_tag: Int32 = 0x0  # 0x08  # Always 0x00 (?)
    version: Int32 = 0x0B  # 0x0C  # Always 0x0B

    pointer_size: Int8  # 0x10  # 4 on WiiU, 8 on Switch
    endian: Int8  # 0x11  # 0 (big) on WiiU, 1 (little) on Switch
    padding_option: Int8  # 0x12  # 0 on WiiU, 1 on Switch
    base_class: Int8  # 0x13  # Always 1

    section_count: Int32 = 3  # 0x14  # Always 3 (classnames, types, data)
    data_section_id: Int32 = 2  # 0x18  # Always 2, refers to __data__ section
    data_section_offset: UInt32 = 0  # 0x1C  # Always 0, beginning offset in __data__
    classnames_section_id: Int32 = 0  # 0x20  # Always 0, refers to __classnames__ section
    classnames_section_offset: UInt32 = 0x4B  # 0x24  # Always 75, offset to hkRootLevelContainer?
    hk_version: str = "hk_2014.2.0-r1"  # 0x28  # Always same, terminated with 0xFF
    flags: Int32 = 0  # 0x38  # Always 0x00 (?)
    max_predicate: Int16 = 21  # 0x3C  # Always 0x15 (?)
    predicate_size_plus_padding: UInt16 = 0  # 0x3E  # 0 or 16; additional data (?)

    unk40: Int16 = 20  # 0x40  # Always 20
    unk42: Int16 = 0  # 0x42  # Always 0 (padding?)
    unk44: Int32 = 0  # 0x44  # Always 0 (padding?)
    unk48: Int32 = 0  # 0x48  # Always 0 (padding?)
    unk4C: Int32 = 0  # 0x4C  # Always 0 (padding?)

    # fmt:on

    def to_switch(self):
        self.pointer_size = 8
        self.endian = 1
        self.padding_option = 1
        self.base_class = 1

    def to_wiiu(self):
        self.pointer_size = 4
        self.endian = 0
        self.padding_option = 0
        self.base_class = 1

    def read(self, br: BinaryReader):
        # Read the header
        self.magic0 = br.assert_uint32(0x57E0E057)
        self.magic1 = br.assert_uint32(0x10C0C010)
        self.user_tag = br.assert_int32(0x0)
        self.version = br.assert_int32(0x0B)

        self.pointer_size = br.assert_int8(4, 8)
        self.endian = br.assert_int8(0, 1)
        self.padding_option = br.assert_int8(0, 1)
        self.base_class = br.assert_int8(1)

        self.section_count = br.assert_int32(3)
        self.data_section_id = br.assert_int32(2)
        self.data_section_offset = br.assert_uint32(0x0)

        self.classnames_section_id = br.assert_int32(0)
        self.classnames_section_offset = br.assert_uint32(0x4B)
        self.hk_version = br.assert_string("hk_2014.2.0-r1", size=15)
        br.assert_uint8(0xFF)

        self.flags = br.assert_int32(0x0)
        self.max_predicate = br.assert_int16(0x15)
        self.predicate_size_plus_padding = br.assert_uint16(0, 16)

        if self.predicate_size_plus_padding == 0:
            pass
        elif self.predicate_size_plus_padding == 16:
            self.unk40 = br.assert_int16(0x14)
            self.unk42 = br.assert_int16(0x0)
            self.unk44 = br.assert_int32(0x0)
            self.unk48 = br.assert_int32(0x0)
            self.unk4C = br.assert_int32(0x0)
        else:
            raise NotImplementedError("Invalid predicate size? Idk really")

    def write(self, bw: BinaryWriter):
        bw.write_uint32(self.magic0)
        bw.write_uint32(self.magic1)
        bw.write_int32(self.user_tag)
        bw.write_int32(self.version)

        bw.write_int8(self.pointer_size)
        bw.write_int8(self.endian)
        bw.write_int8(self.padding_option)
        bw.write_int8(self.base_class)
        bw.write_int32(self.section_count)
        bw.write_int32(self.data_section_id)
        bw.write_uint32(self.data_section_offset)

        bw.write_int32(self.classnames_section_id)
        bw.write_uint32(self.classnames_section_offset)
        bw.write_string(self.hk_version, size=15)
        bw.write_uint8(UInt8(0xFF))

        bw.write_int32(self.flags)
        bw.write_int16(self.max_predicate)
        bw.write_uint16(self.predicate_size_plus_padding)

        if self.predicate_size_plus_padding == 16:
            bw.write_int16(self.unk40)
            bw.write_int16(self.unk42)
            bw.write_int32(self.unk44)
            bw.write_int32(self.unk48)
            bw.write_int32(self.unk4C)

    def as_dict(self):
        if self.predicate_size_plus_padding == 16:
            return {
                "unk40": self.unk40,
                "unk42": self.unk42,
                "unk44": self.unk44,
                "unk48": self.unk48,
                "unk4C": self.unk4C,
            }
        elif self.predicate_size_plus_padding == 0:
            return None
        else:
            raise NotImplementedError()

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        if d:
            inst.predicate_size_plus_padding = UInt16(16)
            inst.unk40, inst.unk42, inst.unk44, inst.unk48, inst.unk4C = d.values()

        return inst

    def __repr__(self):
        return f"{self.__class__.__name__}({self.pointer_size}, {self.endian}, {self.padding_option}, {self.base_class}, {self.predicate_size_plus_padding})"
