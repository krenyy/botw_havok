from ..binary import BinaryReader, BinaryWriter
from ..container.sections.util import GlobalReference, LocalFixup
from .base import HKBase
from .common.hkReferencedObject import hkReferencedObject
from .hkpPhysicsSystem import hkpPhysicsSystem
from typing import List

if False:
    from ..hk import HK
    from ..container.sections.data import HKObject


class hkpPhysicsData(HKBase, hkReferencedObject):
    """Physics data container, contains references
    to world info physics systems
    """

    # worldCinfo: hkpWorldCinfo  # Doesn't seem to be used in BotW (?)
    systems: List[hkpPhysicsSystem]

    def __init__(self):
        super().__init__()  # HKBase

        self.systems = []

    def deserialize(self, hk: "HK", obj: "HKObject"):
        HKBase.deserialize(self, hk, obj)

        br = BinaryReader(obj.bytes)
        br.big_endian = hk.header.endian == 0

        # Read base referenced object data
        hkReferencedObject.deserialize(self, hk, br)
        if hk.header.padding_option:
            br.align_to(16)

        # worldCinfo_offset = br.tell()
        hk._assert_pointer(br)

        # systemCount_offset = br.tell()
        systemCount = hk._read_counter(br)
        br.align_to(16)

        # systems_offset = br.read()
        for gr in obj.global_references:
            if gr.src_rel_offset == br.tell():
                hk.data.objects.remove(gr.dst_obj)

                system = hkpPhysicsSystem()
                self.systems.append(system)
                system.deserialize(hk, gr.dst_obj)

                hk._assert_pointer(br)
        br.align_to(16)

        obj.local_fixups.clear()
        obj.global_references.clear()

    def serialize(self, hk: "HK"):
        HKBase.assign_class(self, hk)

        bw = BinaryWriter()
        bw.big_endian = hk.header.endian == 0

        hkReferencedObject.serialize(self, hk, bw)
        if hk.header.padding_option:
            bw.align_to(16)

        # worldCinfo_offset = bw.tell()
        hk._write_empty_pointer(bw)

        systemCount_offset = bw.tell()
        hk._write_counter(bw, len(self.systems))
        bw.align_to(16)

        systems_offset = bw.tell()
        for system in self.systems:
            hk.data.objects.append(system.hkobj)
            system.serialize(hk)

            gr = GlobalReference()
            gr.src_obj = self.hkobj
            gr.src_rel_offset = bw.tell()
            gr.dst_obj = system.hkobj
            self.hkobj.global_references.append(gr)

            hk._write_empty_pointer(bw)
        bw.align_to(16)

        self.hkobj.local_fixups = [LocalFixup(systemCount_offset, systems_offset)]

        HKBase.serialize(self, hk, bw)

    def asdict(self):
        d = super().asdict()
        d.update(hkReferencedObject.asdict(self))
        d.update(
            {
                # "worldCinfo": self.worldCinfo,
                "systems": [ps.asdict() for ps in self.systems],
            }
        )

        return d

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()
        # inst.worldCinfo = d['worldCinfo']
        inst.systems = [hkpPhysicsSystem.fromdict(ps) for ps in d["systems"]]
        inst.__dict__.update(HKBase.fromdict(d).__dict__)
        inst.__dict__.update(hkReferencedObject.fromdict(d).__dict__)

        return inst

    def __repr__(self):
        return f"{self.__class__.__name__}({self.systems})"
