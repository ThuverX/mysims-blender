# hkClassType.py
from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING, Union

# Forward-only typing to avoid import cycles; adjust the import paths if needed.
if TYPE_CHECKING:
    from .classes.hkPhysicsData import hkPhysicsDataClass
    from .classes.shapes.hkSphereShape import hkSphereShapeClass
    from .classes.shapes.hkMoppBvTreeShape import hkMoppBvTreeShapeClass
    from .classes.shapes.hkSimpleMeshShape import hkSimpleMeshShapeClass

# Matches the C++ hkClassVariant union of pointers to specific class types.
hkClassVariant = Union[
    "hkPhysicsDataClass",
    "hkSphereShapeClass",
    "hkMoppBvTreeShapeClass",
    "hkSimpleMeshShapeClass",
]

class hkClassType(IntEnum):
    hkClass = 0xA52796EB
    hkClassMember = 0x2E50284B
    hkClassEnum = 0x9617A10C
    hkClassEnumItem = 0xCE6F8A6C
    hkWorldCinfo = 0x804C9B06
    hkAabb = 0x4A948B16
    hkCdBody = 0xE94D2688
    hkSweptTransform = 0x0B4E5770
    hkConstraintData = 0xF28AB3B7
    hkPhantom = 0x9D6E0200
    hkEntityDeactivator = 0xDA8C7D7D
    hkPhysicsData = 0xC2A461E4
    hkPhysicsSystem = 0x3ACE2C22
    hkMotion = 0x179F1A0B
    hkAction = 0x95F58619
    hkShapeCollection = 0xD5F6B4EF
    hkSimpleMeshShape = 0x33711D3B
    hkMoppBvTreeShape = 0x83EB786F
    hkRigidBody = 0xEA24A665
    hkBvTreeShape = 0xE7260682
    hkMoppCodeCodeInfo = 0xD8FDBB08
    hkConstraintAtom = 0x6DAC429E
    hkReferencedObject = 0x3B1C1113
    hkWorldMemoryWatchDog = 0x3456CB8A
    # hkShapeContainer = 0xE0708A00,  # intentionally commented in the original
    hkCollidable = 0x3606426D
    hkBroadPhaseHandle = 0xFA5860DA
    hkEntity = 0x32C2E1AD
    hkSimpleMeshShapeTriangle = 0xE3D19F47
    hkCollisionFilter = 0xB6FA76F0
    hkMaterial = 0x0485A264
    hkKeyframedRigidMotion = 0x27F50BFA
    hkMoppCode = 0xBD097996
    hkBaseObject = 0xE0708A00
    hkMaxSizeMotion = 0xD9314173
    hkPropertyValue = 0xC75925AA
    hkShape = 0x9AB27645
    hkTypedBroadPhaseHandle = 0x386F6DE0
    hkModifierConstraintAtom = 0xC85D520F
    hkSingleShapeContainer = 0x73AA1D38
    hkMultiThreadLock = 0x7497262B
    hkWorldObject = 0x7107DE4E
    hkConstraintInstance = 0x2D0D9C11
    hkProperty = 0x9CE308E9
    hkMotionState = 0x332F16FA
    hkLinkedCollidable = 0x3E51C7FC
    hkSphereShape = 0xAB396039


# Convenience maps and helpers

CLASS_ID_TO_NAME = {member.value: member.name for member in hkClassType}
CLASS_NAME_TO_ID = {member.name: member.value for member in hkClassType}

def hk_class_type_from_id(value: int) -> hkClassType | None:
    try:
        return hkClassType(value)
    except ValueError:
        return None