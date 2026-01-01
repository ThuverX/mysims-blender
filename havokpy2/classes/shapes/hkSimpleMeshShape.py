from dataclasses import dataclass, field
from typing import List
from ...BinReader import BinReader
from ...hkCommon import hkSimpleMeshShape, hkVector4, hkSimpleMeshShapeTriangle
from ...hkMacros import array_foreach

@dataclass
class hkSimpleMeshShapeClass:
    hkSimpleMeshShape: "hkSimpleMeshShape" = field(default_factory=hkSimpleMeshShape)
    vertices: List[hkVector4] = field(default_factory=list)
    triangles: List[hkSimpleMeshShapeTriangle] = field(default_factory=list)
    materialIndices: List[int] = field(default_factory=list)

    @staticmethod
    def read(obj: "hkSimpleMeshShapeClass", reader: BinReader, section):
        hkSimpleMeshShape.read(obj.hkSimpleMeshShape, reader)

        def _vert(i: int):
            v = hkVector4()
            hkVector4.read(v, reader)
            obj.vertices.append(v)

        def _tri(i: int):
            t = hkSimpleMeshShapeTriangle()
            hkSimpleMeshShapeTriangle.read(t, reader)
            obj.triangles.append(t)

        def _mat(i: int):
            obj.materialIndices.append(reader.read_u8())

        array_foreach(obj.hkSimpleMeshShape.vertices, reader, section, _vert)
        array_foreach(obj.hkSimpleMeshShape.triangles, reader, section, _tri)
        array_foreach(obj.hkSimpleMeshShape.materialIndices, reader, section, _mat)