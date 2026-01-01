from dataclasses import dataclass, field
from typing import Dict, List, Optional, TypeVar, Generic
from .BinReader import BinReader

POINTER_SIZE = 4

@dataclass
class hkPointer:
    ptr: int = 0

    @staticmethod
    def read(pointer: "hkPointer", reader: BinReader):
        pointer.ptr = reader.tell()
        reader.read_u32()
        # Potentially 64-bit pointer padding not handled; matches source.

T = TypeVar('T')

@dataclass
class hkArray(Generic[T]):
    first: hkPointer = field(default_factory=hkPointer)
    count: int = 0
    capacity: int = 0
    flags: int = 0

    @staticmethod
    def read(arr: "hkArray", reader: BinReader):
        hkPointer.read(arr.first, reader)
        arr.count = reader.read_u32()
        arr.capacity = reader.read_u16()
        arr.flags = reader.read_u16()

@dataclass
class hkBaseObject:
    vtable: hkPointer = field(default_factory=hkPointer)

    @staticmethod
    def read(obj: "hkBaseObject", reader: BinReader):
        hkPointer.read(obj.vtable, reader)

@dataclass
class hkReferencedObject(hkBaseObject):
    memSizeAndFlags: int = 0
    referenceCount: int = 0

    @staticmethod
    def read(obj: "hkReferencedObject", reader: BinReader):
        hkBaseObject.read(obj, reader)
        obj.memSizeAndFlags = reader.read_u16()
        obj.referenceCount = reader.read_u16()

@dataclass
class hkMatrix3:
    m: List[float] = field(default_factory=lambda: [0.0]*12)

    @staticmethod
    def read(mtx: "hkMatrix3", reader: BinReader):
        mtx.m = [reader.read_f32() for _ in range(12)]

@dataclass
class hkVector4:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    w: float = 0.0

    @staticmethod
    def read(vec: "hkVector4", reader: BinReader):
        vec.x = reader.read_f32()
        vec.y = reader.read_f32()
        vec.z = reader.read_f32()
        vec.w = reader.read_f32()

@dataclass
class hkCdBody:
    shape: hkPointer = field(default_factory=hkPointer)
    shapeKey: int = 0
    motion: hkPointer = field(default_factory=hkPointer)
    parent: hkPointer = field(default_factory=hkPointer)

    @staticmethod
    def read(obj: "hkCdBody", reader: BinReader):
        hkPointer.read(obj.shape, reader)
        obj.shapeKey = reader.read_u32()
        hkPointer.read(obj.motion, reader)
        hkPointer.read(obj.parent, reader)

@dataclass
class hkBroadPhaseHandle:
    id: int = 0

    @staticmethod
    def read(obj: "hkBroadPhaseHandle", reader: BinReader):
        obj.id = reader.read_u32()

@dataclass
class hkTypedBroadPhaseHandle(hkBroadPhaseHandle):
    type: int = 0
    ownerOffset: int = 0
    objectQualityType: int = 0
    collisionFilterInfo: int = 0

    @staticmethod
    def read(obj: "hkTypedBroadPhaseHandle", reader: BinReader):
        hkBroadPhaseHandle.read(obj, reader)
        obj.type = reader.read_u8()
        obj.ownerOffset = reader.read_u8()
        obj.objectQualityType = reader.read_u16()
        obj.collisionFilterInfo = reader.read_u32()

@dataclass
class hkCollidable(hkCdBody):
    ownerOffset: int = 0
    broadPhaseHandle: hkTypedBroadPhaseHandle = field(default_factory=hkTypedBroadPhaseHandle)
    allowedPenetrationDepth: float = 0.0

    @staticmethod
    def read(obj: "hkCollidable", reader: BinReader):
        hkCdBody.read(obj, reader)
        obj.ownerOffset = reader.read_u32()
        hkTypedBroadPhaseHandle.read(obj.broadPhaseHandle, reader)
        obj.allowedPenetrationDepth = reader.read_f32()

@dataclass
class hkLinkedCollidable(hkCollidable):
    collisionEntries: hkArray[int] = field(default_factory=hkArray)

    @staticmethod
    def read(obj: "hkLinkedCollidable", reader: BinReader):
        hkCollidable.read(obj, reader)
        hkArray.read(obj.collisionEntries, reader)

@dataclass
class hkMultiThread:
    threadId: int = 0
    lockCount: int = 0
    lockBitStack: int = 0

    @staticmethod
    def read(obj: "hkMultiThread", reader: BinReader):
        obj.threadId = reader.read_u32()
        obj.lockCount = reader.read_u16()
        obj.lockBitStack = reader.read_u16()

@dataclass
class hkProperty:
    key: int = 0
    value: int = 0

    @staticmethod
    def read(obj: "hkProperty", reader: BinReader):
        obj.key = reader.read_u32()
        reader.skip(4)
        obj.value = reader.read_u64()

@dataclass
class hkWorldObject(hkReferencedObject):
    world: hkPointer = field(default_factory=hkPointer)
    userData: int = 0
    name: hkPointer = field(default_factory=hkPointer)
    multithreadLock: hkMultiThread = field(default_factory=hkMultiThread)
    collidable: hkLinkedCollidable = field(default_factory=hkLinkedCollidable)
    properties: hkArray[hkProperty] = field(default_factory=hkArray)

    @staticmethod
    def read(obj: "hkWorldObject", reader: BinReader):
        hkReferencedObject.read(obj, reader)
        hkPointer.read(obj.world, reader)
        obj.userData = reader.read_u32()
        hkPointer.read(obj.name, reader)
        hkMultiThread.read(obj.multithreadLock, reader)
        hkLinkedCollidable.read(obj.collidable, reader)
        hkArray.read(obj.properties, reader)

@dataclass
class hkMaterial:
    responseType: int = 0
    friction: float = 0.0
    restitution: float = 0.0

    @staticmethod
    def read(obj: "hkMaterial", reader: BinReader):
        obj.responseType = reader.read_u8()
        reader.skip(3)
        obj.friction = reader.read_f32()
        obj.restitution = reader.read_f32()

@dataclass
class hkTransform:
    rotation: hkMatrix3 = field(default_factory=hkMatrix3)
    translation: hkVector4 = field(default_factory=hkVector4)

    @staticmethod
    def read(obj: "hkTransform", reader: BinReader):
        hkMatrix3.read(obj.rotation, reader)
        hkVector4.read(obj.translation, reader)

@dataclass
class hkMotionState:
    transform: hkTransform = field(default_factory=hkTransform)
    sweptTransform: bytes = b""
    deltaAngle: hkVector4 = field(default_factory=hkVector4)
    objectRadius: float = 0.0
    maxLinearVelocity: float = 0.0
    maxAngularVelocity: float = 0.0
    linearDamping: float = 0.0
    angularDamping: float = 0.0
    deactivationClass: int = 0
    deactivationCounter: int = 0

    @staticmethod
    def read(obj: "hkMotionState", reader: BinReader):
        hkTransform.read(obj.transform, reader)
        obj.sweptTransform = reader.read_bytes(80)
        hkVector4.read(obj.deltaAngle, reader)
        obj.objectRadius = reader.read_f32()
        obj.maxLinearVelocity = reader.read_f32()
        obj.maxAngularVelocity = reader.read_f32()
        obj.linearDamping = reader.read_f32()
        obj.angularDamping = reader.read_f32()
        obj.deactivationClass = reader.read_u16()
        obj.deactivationCounter = reader.read_u16()
        reader.skip(10)

@dataclass
class hkMotion(hkReferencedObject):
    type: int = 0
    motionState: hkMotionState = field(default_factory=hkMotionState)
    inertiaAndMassInv: hkVector4 = field(default_factory=hkVector4)
    linearVelocity: hkVector4 = field(default_factory=hkVector4)
    angularVelocity: hkVector4 = field(default_factory=hkVector4)

    @staticmethod
    def read(obj: "hkMotion", reader: BinReader):
        hkReferencedObject.read(obj, reader)
        obj.type = reader.read_u8()
        reader.skip(7)
        hkMotionState.read(obj.motionState, reader)
        hkVector4.read(obj.inertiaAndMassInv, reader)
        hkVector4.read(obj.linearVelocity, reader)
        hkVector4.read(obj.angularVelocity, reader)
        reader.skip(16)

@dataclass
class hkEntity(hkWorldObject):
    simulationIsland: hkPointer = field(default_factory=hkPointer)
    material: hkMaterial = field(default_factory=hkMaterial)
    deactivator: hkPointer = field(default_factory=hkPointer)
    constraintsMaster: hkArray[int] = field(default_factory=hkArray)
    constraintsSlave: hkArray[int] = field(default_factory=hkArray)
    constraintRuntime: hkArray[int] = field(default_factory=hkArray)
    storageIndex: int = 0
    processContactCallbackDelay: int = 0
    autoRemoveLevel: int = 0
    motion: hkMotion = field(default_factory=hkMotion)
    solverData: int = 0
    collisionListeners: hkArray[int] = field(default_factory=hkArray)
    activationListeners: hkArray[int] = field(default_factory=hkArray)
    entityListeners: hkArray[int] = field(default_factory=hkArray)
    actions: hkArray[int] = field(default_factory=hkArray)
    uid: int = 0

    @staticmethod
    def read(obj: "hkEntity", reader: BinReader):
        hkWorldObject.read(obj, reader)
        hkPointer.read(obj.simulationIsland, reader)
        hkMaterial.read(obj.material, reader)
        hkPointer.read(obj.deactivator, reader)
        hkArray.read(obj.constraintsMaster, reader)
        hkArray.read(obj.constraintsSlave, reader)
        hkArray.read(obj.constraintRuntime, reader)
        obj.storageIndex = reader.read_u16()
        obj.processContactCallbackDelay = reader.read_u16()
        obj.autoRemoveLevel = reader.read_u8()
        reader.skip(11)
        hkMotion.read(obj.motion, reader)
        obj.solverData = reader.read_u32()
        hkArray.read(obj.collisionListeners, reader)
        hkArray.read(obj.activationListeners, reader)
        hkArray.read(obj.entityListeners, reader)
        hkArray.read(obj.actions, reader)
        obj.uid = reader.read_u32()

@dataclass
class hkPhysicsSystem(hkReferencedObject):
    rigidBodies: hkArray = field(default_factory=hkArray)
    constraints: hkArray = field(default_factory=hkArray)
    actions: hkArray = field(default_factory=hkArray)
    phantoms: hkArray = field(default_factory=hkArray)
    name: hkPointer = field(default_factory=hkPointer)
    userData: hkPointer = field(default_factory=hkPointer)
    active: bool = False

    @staticmethod
    def read(obj: "hkPhysicsSystem", reader: BinReader):
        hkReferencedObject.read(obj, reader)
        hkArray.read(obj.rigidBodies, reader)
        hkArray.read(obj.constraints, reader)
        hkArray.read(obj.actions, reader)
        hkArray.read(obj.phantoms, reader)
        hkPointer.read(obj.name, reader)
        hkPointer.read(obj.userData, reader)
        obj.active = reader.read_u8() != 0
        reader.skip(3)

@dataclass
class hkPhysicsData(hkReferencedObject):
    worldCinfo: hkPointer = field(default_factory=hkPointer)
    systemsArray: hkArray = field(default_factory=hkArray)

    @staticmethod
    def read(obj: "hkPhysicsData", reader: BinReader):
        hkReferencedObject.read(obj, reader)
        hkPointer.read(obj.worldCinfo, reader)
        hkArray.read(obj.systemsArray, reader)

@dataclass
class hkShape(hkReferencedObject):
    userData: int = 0

    @staticmethod
    def read(obj: "hkShape", reader: BinReader):
        hkReferencedObject.read(obj, reader)
        obj.userData = reader.read_u32()

@dataclass
class hkSphereShape(hkShape):
    radius: float = 0.0

    @staticmethod
    def read(obj: "hkSphereShape", reader: BinReader):
        hkShape.read(obj, reader)
        obj.radius = reader.read_f32()

@dataclass
class hkShapeContainer:
    vtable: hkPointer = field(default_factory=hkPointer)

    @staticmethod
    def read(obj: "hkShapeContainer", reader: BinReader):
        hkPointer.read(obj.vtable, reader)

@dataclass
class hkSingleShapeContainer(hkShapeContainer):
    childShape: hkPointer = field(default_factory=hkPointer)

    @staticmethod
    def read(obj: "hkSingleShapeContainer", reader: BinReader):
        hkShapeContainer.read(obj, reader)
        hkPointer.read(obj.childShape, reader)

@dataclass
class hkBvTreeShape(hkShape):
    child: hkSingleShapeContainer = field(default_factory=hkSingleShapeContainer)

    @staticmethod
    def read(obj: "hkBvTreeShape", reader: BinReader):
        hkShape.read(obj, reader)
        hkSingleShapeContainer.read(obj.child, reader)

@dataclass
class hkMoppCodeCodeInfo:
    offset: hkVector4 = field(default_factory=hkVector4)

    @staticmethod
    def read(obj: "hkMoppCodeCodeInfo", reader: BinReader):
        hkVector4.read(obj.offset, reader)

@dataclass
class hkMoppCode(hkReferencedObject):
    info: hkMoppCodeCodeInfo = field(default_factory=hkMoppCodeCodeInfo)
    data: hkArray = field(default_factory=hkArray)

    @staticmethod
    def read(obj: "hkMoppCode", reader: BinReader):
        hkReferencedObject.read(obj, reader)
        hkMoppCodeCodeInfo.read(obj.info, reader)
        hkArray.read(obj.data, reader)

@dataclass
class hkMoppBvTreeShape(hkBvTreeShape):
    code: hkPointer = field(default_factory=hkPointer)

    @staticmethod
    def read(obj: "hkMoppBvTreeShape", reader: BinReader):
        hkBvTreeShape.read(obj, reader)
        hkPointer.read(obj.code, reader)

@dataclass
class hkShapeCollection(hkShape):
    vtable: hkPointer = field(default_factory=hkPointer)
    disableWelding: bool = False

    @staticmethod
    def read(obj: "hkShapeCollection", reader: BinReader):
        hkShape.read(obj, reader)
        hkPointer.read(obj.vtable, reader)
        obj.disableWelding = reader.read_u8() != 1
        reader.skip(3)

@dataclass
class hkSimpleMeshShapeTriangle:
    a: int = 0
    b: int = 0
    c: int = 0

    @staticmethod
    def read(obj: "hkSimpleMeshShapeTriangle", reader: BinReader):
        obj.a = reader.read_u32()
        obj.b = reader.read_u32()
        obj.c = reader.read_u32()

@dataclass
class hkSimpleMeshShape(hkShapeCollection):
    vertices: hkArray = field(default_factory=hkArray)
    triangles: hkArray = field(default_factory=hkArray)
    materialIndices: hkArray = field(default_factory=hkArray)
    radius: float = 0.0

    @staticmethod
    def read(obj: "hkSimpleMeshShape", reader: BinReader):
        hkShapeCollection.read(obj, reader)
        hkArray.read(obj.vertices, reader)
        hkArray.read(obj.triangles, reader)
        hkArray.read(obj.materialIndices, reader)
        obj.radius = reader.read_f32()