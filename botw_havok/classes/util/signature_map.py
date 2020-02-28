class HKSignatureMap:
    hk_signature_map = {
        "hclBendLinkConstraintSet": 646072151,
        "hclBufferDefinition": 2135579644,
        "hclCapsuleShape": 3708024100,
        "hclClothContainer": 890409259,
        "hclClothData": 2465459642,
        "hclClothState": 2063781147,
        "hclCollidable": 4047530174,
        "hclCopyVerticesOperator": 3873113932,
        "hclGatherAllVerticesOperator": 3664999062,
        "hclLocalRangeConstraintSet": 2186704901,
        "hclMoveParticlesOperator": 3864686620,
        "hclObjectSpaceSkinPOperator": 1634840838,
        "hclScratchBufferDefinition": 2685602348,
        "hclSimClothData": 3859829127,
        "hclSimClothPose": 455429281,
        "hclSimpleMeshBoneDeformOperator": 2161735327,
        "hclSimulateOperator": 1975987983,
        "hclSphereShape": 3615093445,
        "hclStandardLinkConstraintSet": 1114321748,
        "hclStretchLinkConstraintSet": 1114321748,
        "hclTransformSetDefinition": 419251557,
        "hclTransitionConstraintSet": 2633903229,
        "hkaAnimationContainer": 646291276,
        "hkaiDirectedGraphExplicitCost": 788715820,
        "hkaiNavMesh": 1833515995,
        "hkaiStaticTreeNavMeshQueryMediator": 1127882337,
        "hkaRagdollInstance": 1414067300,
        "hkaSkeleton": 4274114267,
        "hkaSkeletonMapper": 2900984988,
        "hkcdStaticAabbTree": 2582171851,
        "hkcdStaticTreeDefaultTreeStorage6": 863196278,
        "hkClass": 869540739,
        "hkClassEnum": 2318797263,
        "hkClassEnumItem": 3463416428,
        "hkClassMember": 2968495897,
        "hkpBoxShape": 3701658023,
        "hkpBvCompressedMeshShape": 2880138163,
        "hkpCapsuleShape": 4255218163,
        "hkpConstraintInstance": 3662473502,
        "hkpConvexVerticesShape": 3256650586,
        "hkpCylinderShape": 4205715208,
        "hkpLimitedHingeConstraintData": 1974134179,
        "hkpPhysicsData": 1202244227,
        "hkpPhysicsSystem": 3016519268,
        "hkpPositionConstraintMotor": 339596288,
        "hkpRagdollConstraintData": 3986049271,
        "hkpRigidBody": 3442371045,
        "hkpSphereShape": 933901001,
        "hkpStaticCompoundShape": 3492349726,
        "hkRootLevelContainer": 661831966,
        "StaticCompoundInfo": 1360372226,
    }

    def __new__(cls):
        raise Exception(f"Class {cls} is not meant to be instantiated")

    @staticmethod
    def get(name: str) -> int:
        try:
            return HKSignatureMap.hk_signature_map[name]
        except KeyError:
            raise Exception(f"Missing signature for class '{name}'")
