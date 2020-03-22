import typing

from ...binary import BinaryReader, BinaryWriter
from .base import HKSection
from ...classes.util.signature_map import HKSignatureMap


class HKClass:
    signature: int
    name: str
    offset: int

    def read(self, csec: "HKClassnamesSection", br: BinaryReader):
        self.signature = br.read_uint32()
        br.assert_int8(0x09)  # Delimiter between class name and signature
        self.offset = br.tell() - csec.absolute_offset
        self.name = br.read_string()

    def write(self, csec: "HKClassnamesSection", bw: BinaryWriter):
        bw.write_uint32(self.signature)
        bw.write_int8(0x09)
        self.offset = bw.tell() - csec.absolute_offset
        bw.write_string(self.name)

    @classmethod
    def from_name(cls, name):
        inst = cls()
        inst.name = name
        inst.signature = HKSignatureMap.get(name)

        return inst

    def __eq__(self, value: "HKClass"):
        return (self.signature == value.signature) and (self.name == value.name)

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.name})>"

    def __hash__(self):
        return hash((self.signature, self.name))


class HKClassnamesSection(HKSection):
    """Havok __classnames__ section
    """

    id: int = 0
    tag: str = "__classnames__"

    classes: typing.List[HKClass]

    def __init__(self):
        self.classes = []

        self.classes.append(HKClass.from_name("hkClass"))
        self.classes.append(HKClass.from_name("hkClassMember"))
        self.classes.append(HKClass.from_name("hkClassEnum"))
        self.classes.append(HKClass.from_name("hkClassEnumItem"))

    def read(self, br: BinaryReader):
        super().read(br)

        self.classes.clear()

        while br.tell() < self.absolute_offset + self.EOF_offset:
            if br.peek() == b"\xFF":
                break
            cls = HKClass()
            cls.read(self, br)
            self.classes.append(cls)
        br.align_to(16)

    def write(self, bw: BinaryWriter):
        self.absolute_offset = bw.tell()

        for cls in self.classes:
            cls.write(self, bw)
        bw.align_to(16, b"\xFF")

        self.localfixups_offset = bw.tell() - self.absolute_offset
        self.globalfixups_offset = bw.tell() - self.absolute_offset
        self.virtualfixups_offset = bw.tell() - self.absolute_offset
        self.exports_offset = bw.tell() - self.absolute_offset
        self.imports_offset = bw.tell() - self.absolute_offset
        self.EOF_offset = bw.tell() - self.absolute_offset

        bw.fill_uint32(f"{self.tag}abs", self.absolute_offset)
        bw.fill_uint32(f"{self.tag}loc", self.localfixups_offset)
        bw.fill_uint32(f"{self.tag}glob", self.globalfixups_offset)
        bw.fill_uint32(f"{self.tag}virt", self.virtualfixups_offset)
        bw.fill_uint32(f"{self.tag}exp", self.exports_offset)
        bw.fill_uint32(f"{self.tag}imp", self.imports_offset)
        bw.fill_uint32(f"{self.tag}eof", self.EOF_offset)

    def get(self, value: typing.Union[int, str]):
        """Get Havok class instance

        :param value: Havok class name or offset
        :type value: typing.Union[int, str]
        :raises NotImplementedError: If provided value isn't int or str
        :return: Havok class instance
        :rtype: HKClass
        """
        if isinstance(value, int):
            for cls in self.classes:
                if cls.offset == value:
                    return cls
            else:
                raise Exception(f"HKClass with offset {value} was not found!")

        elif isinstance(value, str):
            for cls in self.classes:
                if cls.name == value:
                    return cls
            else:
                cls = HKClass.from_name(value)
                self.classes.append(cls)
                return cls
        else:
            raise NotImplementedError("Wrong value type provided")

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.classes}>"
