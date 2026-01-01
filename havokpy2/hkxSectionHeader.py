from dataclasses import dataclass, field
from typing import Dict

from .hkxFile import hkxFile
from .BinReader import BinReader

@dataclass
class hkxLocalFixup:
    from_offset: int = 0
    to: int = 0

@dataclass
class hkxGlobalFixup:
    from_offset: int = 0
    section: int = 0
    to: int = 0

@dataclass
class hkxVirtualFixup:
    from_offset: int = 0
    section: int = 0
    classnameOffset: int = 0

@dataclass
class hkxClassname:
    signature: int = 0
    name: str = ""

@dataclass
class hkxSectionHeader:
    sectionTag: bytes = b""
    absoluteDataStart: int = 0
    localFixupsOffset: int = 0
    globalFixupsOffset: int = 0
    virtualFixupsOffset: int = 0
    exportsOffset: int = 0
    importsOffset: int = 0
    bufferSize: int = 0

    fixups: Dict[int, int] = field(default_factory=dict)
    virtualFixups: Dict[int, hkxClassname] = field(default_factory=dict)
    classnames: Dict[int, hkxClassname] = field(default_factory=dict)

    dataOffset: int = 0
    eofOffset: int = 0

    @staticmethod
    def read(obj: "hkxSectionHeader", reader: BinReader, index: int, file: hkxFile):
        obj.sectionTag = reader.read_bytes(19)
        reader.skip(1)

        obj.absoluteDataStart = reader.read_u32()
        obj.localFixupsOffset = reader.read_u32()
        obj.globalFixupsOffset = reader.read_u32()
        obj.virtualFixupsOffset = reader.read_u32()
        obj.exportsOffset = reader.read_u32()
        obj.importsOffset = reader.read_u32()
        obj.bufferSize = reader.read_u32()

        virtualEOF = obj.exportsOffset if obj.exportsOffset != 0xFFFFFFFF else obj.importsOffset
        obj.dataOffset = file.baseOffset + obj.absoluteDataStart
        obj.eofOffset = obj.dataOffset + virtualEOF

        jump = reader.tell()

        if index == file.header.contentsClassNameSectionIndex:
            reader.seek(obj.dataOffset)
            while reader.tell() < obj.eofOffset:
                classname = hkxClassname()
                classname.signature = reader.read_u32()
                reader.skip(1)
                offset = reader.tell() - obj.dataOffset
                classname.name = reader.read_cstring()
                if classname.signature != 0xFFFF:
                    obj.classnames[offset] = classname

        reader.seek(jump)