from ..base import HKBase
from ..hkpBvCompressedMeshShape import hkpBvCompressedMeshShape
from ..hkpPhysicsData import hkpPhysicsData
from ..hkpPhysicsSystem import hkpPhysicsSystem
from ..hkpRigidBody import hkpRigidBody
from ..hkpStaticCompoundShape import hkpStaticCompoundShape
from ..hkRootLevelContainer import hkRootLevelContainer
from ..StaticCompoundInfo import StaticCompoundInfo


class HKClassMap:
    hk_class_map = {
        "hkpBvCompressedMeshShape": hkpBvCompressedMeshShape,
        "hkpRigidBody": hkpRigidBody,
        "hkpPhysicsData": hkpPhysicsData,
        "hkpPhysicsSystem": hkpPhysicsSystem,
        "hkRootLevelContainer": hkRootLevelContainer,
        "StaticCompoundInfo": StaticCompoundInfo,
        "hkpStaticCompoundShape": hkpStaticCompoundShape,
    }

    def __new__(cls):
        raise Exception("This class shouldn't be instantiated")

    @staticmethod
    def get(name: str) -> HKBase:
        try:
            return HKClassMap.hk_class_map[name]
        except KeyError:
            raise NotImplementedError(f"Class '{name}' is not implemented yet!")
