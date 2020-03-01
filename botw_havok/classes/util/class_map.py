from ..base import HKBase
from ..hkpBoxShape import hkpBoxShape
from ..hkpBvCompressedMeshShape import hkpBvCompressedMeshShape
from ..hkpCapsuleShape import hkpCapsuleShape
from ..hkpConvexVerticesShape import hkpConvexVerticesShape
from ..hkpCylinderShape import hkpCylinderShape
from ..hkpPhysicsData import hkpPhysicsData
from ..hkpPhysicsSystem import hkpPhysicsSystem
from ..hkpRigidBody import hkpRigidBody
from ..hkpStaticCompoundShape import hkpStaticCompoundShape
from ..hkRootLevelContainer import hkRootLevelContainer
from ..StaticCompoundInfo import StaticCompoundInfo


class HKClassMap:
    hk_class_map = {
        "hkpBoxShape": hkpBoxShape,
        "hkpBvCompressedMeshShape": hkpBvCompressedMeshShape,
        "hkpCapsuleShape": hkpCapsuleShape,
        "hkpConvexVerticesShape": hkpConvexVerticesShape,
        "hkpCylinderShape": hkpCylinderShape,
        "hkpPhysicsData": hkpPhysicsData,
        "hkpPhysicsSystem": hkpPhysicsSystem,
        "hkpRigidBody": hkpRigidBody,
        "hkpStaticCompoundShape": hkpStaticCompoundShape,
        "hkRootLevelContainer": hkRootLevelContainer,
        "StaticCompoundInfo": StaticCompoundInfo,
    }

    def __new__(cls):
        raise Exception("This class shouldn't be instantiated")

    @staticmethod
    def get(name: str) -> HKBase:
        try:
            return HKClassMap.hk_class_map[name]
        except KeyError:
            raise NotImplementedError(f"Class '{name}' is not implemented yet!")
