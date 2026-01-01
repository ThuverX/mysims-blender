from dataclasses import dataclass, field
from typing import List
from .BinReader import BinReader
from .hkxFile import hkxFile

@dataclass
class HavokFileHeader:
    magic: bytes = b""
    version: int = 0

    @staticmethod
    def read(obj: "HavokFileHeader", reader: BinReader):
        obj.magic = reader.read_bytes(4)
        obj.version = reader.read_u32()

@dataclass
class HavokFile:
    header: HavokFileHeader = field(default_factory=HavokFileHeader)
    fileEntries: List[hkxFile] = field(default_factory=list)

    @staticmethod
    def read(obj: "HavokFile", reader: BinReader):
        HavokFileHeader.read(obj.header, reader)
        while reader.tell() < reader.size():
            reader.skip(4)
            size = reader.read_u32()
            end = reader.tell() + size
            f = hkxFile()
            hkxFile.read(f, reader)
            obj.fileEntries.append(f)
            reader.seek(end)

class HavokFileReader:
    def __init__(self):
        self.result: HavokFile = HavokFile()

    def read(self, buf):
        br = BinReader(buf, little_endian=True)
        HavokFile.read(self.result, br)
        return self.result

    def write(self, buf):
        raise NotImplementedError("Writing not implemented")