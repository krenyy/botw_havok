from .hkpPhysicsData import HKPPhysicsData
from .hkRootLevelContainer import HKRootLevelContainer
from .StaticCompoundInfo import StaticCompoundInfo

class_signature_map = {
    "hkRootLevelContainer": 1234567,
    "hkpPhysicsData": 1234567,
    "hkpPhysicsSystem": 1234567,
    "StaticCompoundInfo": 1234567,
}

class_hk_map = {
    "hkRootLevelContainer": HKRootLevelContainer,
    "hkpPhysicsData": HKPPhysicsData,
    "hkpPhysicsSystem": None,
    "StaticCompoundInfo": StaticCompoundInfo,
}
