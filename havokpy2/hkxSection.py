from dataclasses import dataclass, field
from typing import Optional, Any
from .BinReader import BinReader
from .hkxSectionHeader import hkxSectionHeader
from .hkxFile import hkxFile
from .hkFactory import read_hk_class
from .hkCommon import POINTER_SIZE

@dataclass
class hkxSection:
    root: Optional[Any] = None
    index: int = 0
    file: hkxFile = None
    sectionHeader: hkxSectionHeader = None

    @staticmethod
    def read(obj: "hkxSection", reader: BinReader):
        jump = reader.tell()

        virtualEOF = obj.sectionHeader.exportsOffset if obj.sectionHeader.exportsOffset != 0xFFFFFFFF else obj.sectionHeader.importsOffset

        numLocalFixups = (obj.sectionHeader.globalFixupsOffset - obj.sectionHeader.localFixupsOffset) // 8
        numGlobalFixups = (obj.sectionHeader.virtualFixupsOffset - obj.sectionHeader.globalFixupsOffset) // 12
        numVirtualFixups = (virtualEOF - obj.sectionHeader.virtualFixupsOffset) // 12

        obj.sectionHeader.dataOffset = obj.file.baseOffset + obj.sectionHeader.absoluteDataStart
        obj.sectionHeader.eofOffset = obj.sectionHeader.dataOffset + virtualEOF

        localFixupsOffset = obj.sectionHeader.dataOffset + obj.sectionHeader.localFixupsOffset
        globalFixupsOffset = obj.sectionHeader.dataOffset + obj.sectionHeader.globalFixupsOffset
        virtualFixupsOffset = obj.sectionHeader.dataOffset + obj.sectionHeader.virtualFixupsOffset

        reader.seek(localFixupsOffset)
        for i in range(numLocalFixups):
            f = reader.read_u32()
            t = reader.read_u32()
            if t == 0xFFFFFFFF or f == 0xFFFFFFFF:
                continue
            absoluteTo = obj.sectionHeader.dataOffset + t
            absoluteFrom = f + obj.sectionHeader.dataOffset
            obj.sectionHeader.fixups[absoluteFrom] = absoluteTo

        reader.seek(globalFixupsOffset)
        for i in range(numGlobalFixups):
            f = reader.read_u32()
            section = reader.read_u32()
            to = reader.read_u32()
            if to == 0xFFFFFFFF or f == 0xFFFFFFFF:
                continue
            absoluteTo = obj.file.sectionHeaders[section].dataOffset + to
            absoluteFrom = f + obj.sectionHeader.dataOffset
            obj.sectionHeader.fixups[absoluteFrom] = absoluteTo

        reader.seek(virtualFixupsOffset)
        for i in range(numVirtualFixups):
            f = reader.read_u32()
            section = reader.read_u32()
            cname_off = reader.read_u32()
            if f == 0xFFFFFFFF:
                continue
            classname = obj.file.sectionHeaders[section].classnames.get(cname_off)
            absoluteFrom = f + obj.sectionHeader.dataOffset
            if classname is not None:
                obj.sectionHeader.virtualFixups[absoluteFrom] = classname

        reader.seek(obj.sectionHeader.dataOffset)

        if obj.index == obj.file.header.contentsSectionIndex:
            classname = obj.sectionHeader.virtualFixups.get(reader.tell())
            if classname:
                obj.root = read_hk_class(classname, reader, obj)

        reader.seek(jump)