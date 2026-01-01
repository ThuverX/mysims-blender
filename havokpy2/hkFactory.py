from typing import Optional, Any
from .BinReader import BinReader
from .hkClassType import hkClassType
from .hkxSectionHeader import hkxClassname
from .classes.hkPhysicsData import hkPhysicsDataClass
from .classes.shapes.hkMoppBvTreeShape import hkMoppBvTreeShapeClass
from .classes.shapes.hkSimpleMeshShape import hkSimpleMeshShapeClass
from .classes.shapes.hkSphereShape import hkSphereShapeClass

def read_hk_class(classname: hkxClassname, reader: BinReader, section: "hkxSection") -> Optional[Any]:
    sig = classname.signature
    try:
        cls = hkClassType(sig)
    except ValueError:
        return None

    if cls == hkClassType.hkPhysicsData:
        obj = hkPhysicsDataClass()
        hkPhysicsDataClass.read(obj, reader, section)
        return obj
    if cls == hkClassType.hkMoppBvTreeShape:
        obj = hkMoppBvTreeShapeClass()
        hkMoppBvTreeShapeClass.read(obj, reader, section)
        return obj
    if cls == hkClassType.hkSphereShape:
        obj = hkSphereShapeClass()
        hkSphereShapeClass.read(obj, reader, section)
        return obj
    if cls == hkClassType.hkSimpleMeshShape:
        obj = hkSimpleMeshShapeClass()
        hkSimpleMeshShapeClass.read(obj, reader, section)
        return obj
    return None