from ..hkpPhysicsData import hkpPhysicsData
from ..hkpPhysicsSystem import hkpPhysicsSystem
from ..hkRootLevelContainer import hkRootLevelContainer
from ..StaticCompoundInfo import StaticCompoundInfo
from ..hkpBvCompressedMeshShape import hkpBvCompressedMeshShape
from ..hkpRigidBody import hkpRigidBody

# from ..hkpStaticCompoundShape import hkpStaticCompoundShape

hk_class_map = {
    "hkpBvCompressedMeshShape": hkpBvCompressedMeshShape,
    "hkpRigidBody": hkpRigidBody,
    "hkpPhysicsData": hkpPhysicsData,
    "hkpPhysicsSystem": hkpPhysicsSystem,
    "hkRootLevelContainer": hkRootLevelContainer,
    "StaticCompoundInfo": StaticCompoundInfo,
    # "hkpStaticCompoundShape": hkpStaticCompoundShape,
}
