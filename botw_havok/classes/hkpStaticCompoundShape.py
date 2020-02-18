from .hkpBvTreeShape import hkpBvTreeShape
from .hkpStaticCompoundShapeInstance import hkpStaticCompoundShapeInstance
from .hkpShapeKeyTable import hkpShapeKeyTable
from hkcdStaticTreeDefaultTreeStorage6 import hkcdStaticTreeDefaultTreeStorage6
from typing import List


class hkpStaticCompoundShape(hkpBvTreeShape):
    numBitsForChildShapeKey: int
    referencePolicy: int
    childShapeKeyMask: int

    instances: List[hkpStaticCompoundShapeInstance]
    instanceExtraInfos: List[int]

    disabledLargeShapeKeyTable: hkpShapeKeyTable
    tree: hkcdStaticTreeDefaultTreeStorage6
