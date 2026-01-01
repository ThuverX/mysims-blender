from dataclasses import dataclass, field
from typing import List
from .BinReader import BinReader

@dataclass
class hkxHeaderlayout:
    bytesInHkPointer: int = 0
    littleEndian: bool = True
    reusePaddingOptimization: bool = False
    emptyBaseClassOptimization: bool = False

@dataclass
class hkxHeader:
    magic1: int = 0
    magic2: int = 0
    userTag: int = 0
    version: int = 0
    layout: hkxHeaderlayout = field(default_factory=hkxHeaderlayout)
    numSections: int = 0
    contentsSectionIndex: int = 0
    contentsSectionOffset: int = 0
    contentsClassNameSectionIndex: int = 0
    contentsClassNameSectionOffset: int = 0
    contentsVersion: bytes = b""
    pad: int = 0
    flags: int = 0
    pad2: int = 0

@dataclass
class hkxFile:
    header: hkxHeader = field(default_factory=hkxHeader)
    sectionHeaders: List["hkxSectionHeader"] = field(default_factory=list)
    sections: List["hkxSection"] = field(default_factory=list)
    baseOffset: int = 0

    @staticmethod
    def read(obj: "hkxFile", reader: BinReader):
        obj.baseOffset = reader.tell()

        # Read header
        obj.header.magic1 = reader.read_u32()
        obj.header.magic2 = reader.read_u32()
        obj.header.userTag = reader.read_u32()
        obj.header.version = reader.read_u32()
        obj.header.layout.bytesInHkPointer = reader.read_u8()
        obj.header.layout.littleEndian = reader.read_u8() != 0
        obj.header.layout.reusePaddingOptimization = reader.read_u8() != 0
        obj.header.layout.emptyBaseClassOptimization = reader.read_u8() != 0
        obj.header.numSections = reader.read_u32()
        obj.header.contentsSectionIndex = reader.read_u32()
        obj.header.contentsSectionOffset = reader.read_u32()
        obj.header.contentsClassNameSectionIndex = reader.read_u32()
        obj.header.contentsClassNameSectionOffset = reader.read_u32()
        obj.header.contentsVersion = reader.read_bytes(15)
        obj.header.pad = reader.read_u8()
        obj.header.flags = reader.read_u32()
        obj.header.pad2 = reader.read_u32()

        from .hkxSectionHeader import hkxSectionHeader
        from .hkxSection import hkxSection
        # Section headers
        for i in range(obj.header.numSections):
            sh = hkxSectionHeader()
            hkxSectionHeader.read(sh, reader, i, obj)
            obj.sectionHeaders.append(sh)
        # Sections
        for i in range(obj.header.numSections):
            sec = hkxSection()
            sec.file = obj
            sec.sectionHeader = obj.sectionHeaders[i]
            sec.index = i
            hkxSection.read(sec, reader)
            obj.sections.append(sec)