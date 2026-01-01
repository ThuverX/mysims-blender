from dataclasses import dataclass, field
from ...BinReader import BinReader
from ...hkCommon import hkSphereShape

@dataclass
class hkSphereShapeClass:
    hkSphereShape: "hkSphereShape" = field(default_factory=hkSphereShape)
    radius: float = 0.0

    @staticmethod
    def read(obj: "hkSphereShapeClass", reader: BinReader, section):
        hkSphereShape.read(obj.hkSphereShape, reader)

        obj.radius = obj.hkSphereShape.radius