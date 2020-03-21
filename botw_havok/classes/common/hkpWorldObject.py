from typing import List

from ...binary import BinaryReader, BinaryWriter
from .hkMultiThreadCheck import hkMultiThreadCheck
from .hkpLinkedCollidable import hkpLinkedCollidable
from .hkReferencedObject import hkReferencedObject
from .hkSimpleProperty import hkSimpleProperty

if False:
    from ...hk import HK
    from ...container.sections.hkobject import HKObject


class hkpWorldObject(hkReferencedObject):
    # world: None = None
    userData: int
    collidable: hkpLinkedCollidable
    multiThreadCheck: hkMultiThreadCheck

    _namePointer_offset: int  # for writing
    name: str

    properties: List[hkSimpleProperty]

    def __init__(self):
        self.properties = []

    def deserialize(self, hk: "HK", br: BinaryReader, obj: "HKObject"):
        super().deserialize(hk, br)

        if hk.header.padding_option:
            br.align_to(16)

        world_offset = br.tell()
        hk._assert_pointer(br)

        if hk.header.pointer_size == 8:
            self.userData = br.read_uint64()
        elif hk.header.pointer_size == 4:
            self.userData = br.read_uint32()
        else:
            raise NotImplementedError()

        # ----

        self.collidable = hkpLinkedCollidable()
        self.collidable.deserialize(hk, br, obj)

        self.multiThreadCheck = hkMultiThreadCheck()
        self.multiThreadCheck.deserialize(hk, br)
        if hk.header.padding_option:
            br.align_to(16)

        for lfu in obj.local_fixups:
            if lfu.src == br.tell():
                br.step_in(lfu.dst)
                self.name = br.read_string()
                br.step_out()
                hk._assert_pointer(br)
                break

        propertiesCount_offset = br.tell()
        propertiesCount = hk._read_counter(br)

        # FIXME: Probably not right
        for _ in range(propertiesCount):
            prop = hkSimpleProperty()
            prop.deserialize(hk, br)
            self.properties.append(prop)

    def serialize(self, hk: "HK", bw: BinaryWriter, obj):
        super().serialize(hk, bw)
        if hk.header.padding_option:
            bw.align_to(16)

        world_offset = bw.tell()
        hk._write_empty_pointer(bw)

        if hk.header.pointer_size == 8:
            bw.write_uint64(self.userData)
        elif hk.header.pointer_size == 4:
            bw.write_uint32(self.userData)
        else:
            raise NotImplementedError()

        # ----

        self.collidable.serialize(hk, bw, obj)
        self.multiThreadCheck.serialize(hk, bw)
        if hk.header.padding_option:
            bw.align_to(16)

        self._namePointer_offset = bw.tell()
        hk._write_empty_pointer(bw)  # 'name' pointer

        propertiesCount_offset = bw.tell()
        hk._write_counter(bw, len(self.properties))

        for prop in self.properties:
            prop.serialize(hk, bw)

    def asdict(self):
        d = super().asdict()
        d.update(
            {
                # "world": self.world,
                "userData": self.userData,
                "collidable": self.collidable.asdict(),
                "multiThreadCheck": self.multiThreadCheck.asdict(),
                "name": self.name,
            }
        )

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        inst.memSizeAndRefCount = d["memSizeAndRefCount"]
        # inst.world = d["world"]
        inst.userData = d["userData"]
        inst.collidable = hkpLinkedCollidable.fromdict(d["collidable"])
        inst.multiThreadCheck = hkMultiThreadCheck.fromdict(d["multiThreadCheck"])
        inst.name = d["name"]

        return inst
