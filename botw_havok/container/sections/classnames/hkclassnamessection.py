import typing
from typing import TYPE_CHECKING

import numpy as np

from .hkclass import HKClass
from ..base import HKSection
from ....binary import BinaryReader, BinaryWriter

if TYPE_CHECKING:
    from ....hkfile import HKFile


class HKClassnamesSection(HKSection):
    """Havok __classnames__ section
    """

    id: int = 0
    tag: str = "__classnames__"

    classes: typing.List[HKClass]

    def __init__(self):
        self.classes = [
            HKClass.from_name(x)
            for x in ["hkClass", "hkClassMember", "hkClassEnum", "hkClassEnumItem"]
        ]

    def read(self, hkFile: "HKFile", br: BinaryReader):
        super().read(hkFile, br)

        self.classes.clear()

        while br.tell() < self.absolute_offset + self.EOF_offset:
            if br.peek() == b"\xFF":
                break
            cls = HKClass()
            cls.read(self, br)
            self.classes.append(cls)
        br.align_to(16)

    def write(self, hkFile: "HKFile", bw: BinaryWriter):
        self.absolute_offset = bw.tell()

        for cls in self.classes:
            cls.write(self, bw)
        self.classes.clear()

        bw.align_to(16, b"\xFF")

        self.local_fixups_offset = bw.tell() - self.absolute_offset
        self.global_fixups_offset = self.local_fixups_offset
        self.virtual_fixups_offset = self.global_fixups_offset
        self.exports_offset = self.virtual_fixups_offset
        self.imports_offset = self.exports_offset
        self.EOF_offset = self.imports_offset

        bw.fill_uint32(f"{self.tag}abs", self.absolute_offset)
        bw.fill_uint32(f"{self.tag}loc", self.local_fixups_offset)
        bw.fill_uint32(f"{self.tag}glob", self.global_fixups_offset)
        bw.fill_uint32(f"{self.tag}virt", self.virtual_fixups_offset)
        bw.fill_uint32(f"{self.tag}exp", self.exports_offset)
        bw.fill_uint32(f"{self.tag}imp", self.imports_offset)
        bw.fill_uint32(f"{self.tag}eof", self.EOF_offset)

    def get(self, value: typing.Union[np.integer, str]):
        """Get Havok class instance

        :param value: Havok class name or offset
        :type value: typing.Union[numpy.integer, str]
        :raises NotImplementedError: If provided value has wrong type
        :return: Havok class instance
        :rtype: HKClass
        """
        if isinstance(value, np.integer):
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
