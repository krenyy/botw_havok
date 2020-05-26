from ..StaticCompoundInfo import StaticCompoundInfo
from ..hkRootLevelContainer import hkRootLevelContainer
from ..hkaiDirectedGraphExplicitCost import hkaiDirectedGraphExplicitCost
from ..hkaiNavMesh import hkaiNavMesh
from ..hkaiStaticTreeNavMeshQueryMediator import hkaiStaticTreeNavMeshQueryMediator
from ..hkcdStaticAabbTree import hkcdStaticAabbTree
from ..hkcdStaticTreeDefaultTreeStorage6 import hkcdStaticTreeDefaultTreeStorage6
from ..hkpBoxShape import hkpBoxShape
from ..hkpBvCompressedMeshShape import hkpBvCompressedMeshShape
from ..hkpCapsuleShape import hkpCapsuleShape
from ..hkpConvexTransformShape import hkpConvexTransformShape
from ..hkpConvexTranslateShape import hkpConvexTranslateShape
from ..hkpConvexVerticesShape import hkpConvexVerticesShape
from ..hkpCylinderShape import hkpCylinderShape
from ..hkpListShape import hkpListShape
from ..hkpPhysicsData import hkpPhysicsData
from ..hkpPhysicsSystem import hkpPhysicsSystem
from ..hkpRigidBody import hkpRigidBody
from ..hkpSphereShape import hkpSphereShape
from ..hkpStaticCompoundShape import hkpStaticCompoundShape


class HKClassMap:
    hk_class_map = {
        "hkaiDirectedGraphExplicitCost": hkaiDirectedGraphExplicitCost,
        "hkaiNavMesh": hkaiNavMesh,
        "hkaiStaticTreeNavMeshQueryMediator": hkaiStaticTreeNavMeshQueryMediator,
        "hkcdStaticAabbTree": hkcdStaticAabbTree,
        "hkcdStaticTreeDefaultTreeStorage6": hkcdStaticTreeDefaultTreeStorage6,
        "hkpBoxShape": hkpBoxShape,
        "hkpBvCompressedMeshShape": hkpBvCompressedMeshShape,
        "hkpCapsuleShape": hkpCapsuleShape,
        "hkpConvexTransformShape": hkpConvexTransformShape,
        "hkpConvexTranslateShape": hkpConvexTranslateShape,
        "hkpConvexVerticesShape": hkpConvexVerticesShape,
        "hkpCylinderShape": hkpCylinderShape,
        "hkpListShape": hkpListShape,
        "hkpPhysicsData": hkpPhysicsData,
        "hkpPhysicsSystem": hkpPhysicsSystem,
        "hkpRigidBody": hkpRigidBody,
        "hkpSphereShape": hkpSphereShape,
        "hkpStaticCompoundShape": hkpStaticCompoundShape,
        "hkRootLevelContainer": hkRootLevelContainer,
        "StaticCompoundInfo": StaticCompoundInfo,
    }

    def __new__(cls):
        raise Exception("This class shouldn't be instantiated")

    @staticmethod
    def get(name: str):
        try:
            return HKClassMap.hk_class_map[name]
        except KeyError:
            raise SystemExit(f"Class '{name}' is not implemented yet!")
