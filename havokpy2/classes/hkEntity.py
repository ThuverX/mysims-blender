from dataclasses import dataclass, field
from typing import Optional, Any
from ..BinReader import BinReader
from ..hkCommon import hkEntity
from ..hkMacros import follow_pointer, classname_of


@dataclass
class hkEntityClass:
    hkEntity: "hkEntity" = field(default_factory=hkEntity)
    shape: Optional[Any] = None

    @staticmethod
    def read(obj: "hkEntityClass", reader: BinReader, section):
        from ..hkFactory import read_hk_class
        hkEntity.read(obj.hkEntity, reader)
        def _read():
            cname = classname_of(obj.hkEntity.collidable.shape, section)
            if cname:
                obj.shape = read_hk_class(cname, reader, section)
        follow_pointer(obj.hkEntity.collidable.shape, reader, section, _read)