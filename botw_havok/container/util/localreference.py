from io import BytesIO
from typing import Sequence, Union

from ...binary import BinaryWriter
from ...binary.types import BinaryType, String, UInt32
from ...classes.common.hkObject import hkObject
from ...container.util.localfixup import LocalFixup

if False:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class LocalReference:
    src_offset: UInt32
    dst_bytes: bytes
    align: bool

    def __init__(
        self,
        hkFile: "HKFile",
        bw: BinaryWriter,
        obj: "HKObject",
        offset: UInt32,
        data: Union[hkObject, BinaryType, Sequence[Union[hkObject, BinaryType]]],
    ):
        self.src_offset = offset

        _bw = BinaryWriter(big_endian=hkFile.header.endian == 0)

        if isinstance(data, list):
            hkFile._write_empty_pointer(bw)
            hkFile._write_counter(bw, UInt32(len(data)))

        self._write(hkFile, _bw, obj, data)

        self.dst_bytes = _bw.getvalue()

    def _write(
        self,
        hkFile: "HKFile",
        bw: BinaryWriter,
        obj: "HKObject",
        data: Union[hkObject, BinaryType, Sequence[Union[hkObject, BinaryType]]],
    ):
        if isinstance(data, list):
            for item in data:
                if isinstance(item, String):
                    hkFile._write_empty_pointer(bw)
            for item in data:
                self._write(hkFile, bw, obj, item)
                if isinstance(item, String):
                    bw.align_to(16)
        elif isinstance(data, hkObject):
            data.serialize(hkFile, bw, obj)
        elif isinstance(data, BinaryType):
            bw.write(data)
        else:
            raise NotImplementedError()

    def resolve(self, bw: BinaryWriter, obj: "HKObject"):
        obj.local_fixups.append(LocalFixup(self.src_offset, bw.tell()))

        BytesIO.write(bw, self.dst_bytes)

        bw.align_to(16)
