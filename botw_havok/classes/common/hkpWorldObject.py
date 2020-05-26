from typing import List, Union
from typing import TYPE_CHECKING

from .hkMultiThreadCheck import hkMultiThreadCheck
from .hkReferencedObject import hkReferencedObject
from .hkSimpleProperty import hkSimpleProperty
from .hkpLinkedCollidable import hkpLinkedCollidable
from ...binary import BinaryReader, BinaryWriter
from ...binary.types import UInt32, UInt64

if TYPE_CHECKING:
    from ...hkfile import HKFile
    from ...container.util.hkobject import HKObject


class hkpWorldObject(hkReferencedObject):
    # world: None = None
    userData: Union[UInt32, UInt64]
    collidable: hkpLinkedCollidable
    multiThreadCheck: hkMultiThreadCheck

    name: str

    properties: List[hkSimpleProperty]

    _namePointer_offset: UInt32

    def __init__(self):
        self.properties = []

    def deserialize(self, hkFile: "HKFile", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hkFile, br, obj)

        if hkFile.header.padding_option:
            br.align_to(16)

        hkFile._assert_pointer(br)  # Empty 'world' pointer

        if hkFile.header.pointer_size == 8:
            self.userData = br.read_uint64()
        elif hkFile.header.pointer_size == 4:
            self.userData = br.read_uint32()
        else:
            raise NotImplementedError()

        # ----

        self.collidable = hkpLinkedCollidable()
        self.collidable.deserialize(hkFile, br, obj)

        self.multiThreadCheck = hkMultiThreadCheck()
        self.multiThreadCheck.deserialize(hkFile, br, obj)

        if hkFile.header.padding_option:
            br.align_to(16)

        namePointer_offset = hkFile._assert_pointer(br)

        propertiesCount_offset = hkFile._assert_pointer(br)
        propertiesCount = hkFile._read_counter(br)
        assert propertiesCount == 0

        for lfu in obj.local_fixups:
            br.step_in(lfu.dst)
            if lfu.src == namePointer_offset:
                self.name = br.read_string()
            elif lfu.src == propertiesCount_offset:
                for _ in range(propertiesCount):
                    prop = hkSimpleProperty()
                    prop.deserialize(hkFile, br, obj)

                    self.properties.append(prop)
            br.step_out()

    def serialize(self, hkFile: "HKFile", bw: BinaryWriter, obj: "HKObject"):
        super().serialize(hkFile, bw, obj)

        ###

        if hkFile.header.padding_option:
            bw.align_to(16)

        hkFile._write_empty_pointer(bw)

        if hkFile.header.pointer_size == 8:
            bw.write_uint64(UInt64(self.userData))
        elif hkFile.header.pointer_size == 4:
            bw.write_uint32(UInt32(self.userData))
        else:
            raise NotImplementedError()

        # ----

        self.collidable.serialize(hkFile, bw, obj)
        self.multiThreadCheck.serialize(hkFile, bw, obj)
        if hkFile.header.padding_option:
            bw.align_to(16)

        self._namePointer_offset = hkFile._write_empty_pointer(bw)

        propertiesCount_offset = hkFile._write_empty_pointer(bw)
        hkFile._write_counter(bw, UInt32(len(self.properties)))

        # FIXME: Probably should be in hkpEntity, doesn't seem to cause issues yet
        for prop in self.properties:
            prop.serialize(hkFile, bw, obj)

    def as_dict(self):
        d = super().as_dict()
        d.update(
            {
                # "world": self.world,
                "userData": self.userData,
                "collidable": self.collidable.as_dict(),
                "multiThreadCheck": self.multiThreadCheck.as_dict(),
                "name": self.name,
            }
        )

        return d

    @classmethod
    def from_dict(cls, d: dict):
        inst = cls()
        inst.memSizeAndRefCount = d["memSizeAndRefCount"]
        # inst.world = d["world"]
        inst.userData = d["userData"]
        inst.collidable = hkpLinkedCollidable.from_dict(d["collidable"])
        inst.multiThreadCheck = hkMultiThreadCheck.from_dict(d["multiThreadCheck"])
        inst.name = d["name"]

        return inst
