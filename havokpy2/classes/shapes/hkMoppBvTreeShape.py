from dataclasses import dataclass, field
from typing import Optional, Any
from ...BinReader import BinReader
from ...hkCommon import hkMoppBvTreeShape
from ...hkMacros import follow_pointer, classname_of

@dataclass
class hkMoppBvTreeShapeClass:
    hkMoppBvTreeShape: "hkMoppBvTreeShape" = field(default_factory=hkMoppBvTreeShape)
    childShape: Optional[Any] = None

    @staticmethod
    def read(obj: "hkMoppBvTreeShapeClass", reader: BinReader, section):
        from ...hkFactory import read_hk_class
        hkMoppBvTreeShape.read(obj.hkMoppBvTreeShape, reader)

        def _read():
            cname = classname_of(obj.hkMoppBvTreeShape.child.childShape, section)
            if cname:
                obj.childShape = read_hk_class(cname, reader, section)
        follow_pointer(obj.hkMoppBvTreeShape.child.childShape, reader, section, _read)