from .BinReader import BinReader
from .hkCommon import POINTER_SIZE

def array_foreach(arr, reader: BinReader, section, func):
    if arr.count > 0:
        jump = reader.tell()
        start = section.sectionHeader.fixups.get(arr.first.ptr, 0)
        if start == 0:
            reader.seek(jump)
            return
        reader.seek(start)
        for i in range(arr.count):
            func(i)
        reader.seek(jump)

def array_pointer_foreach(arr, reader: BinReader, section, func):
    if arr.count > 0:
        jump = reader.tell()
        start = section.sectionHeader.fixups.get(arr.first.ptr, 0)
        for i in range(arr.count):
            ptr_loc = start + (i * POINTER_SIZE)
            to = section.sectionHeader.fixups.get(ptr_loc)
            if to is None:
                continue
            reader.seek(to)
            func(i)
        reader.seek(jump)

def follow_pointer(pointer, reader: BinReader, section, func):
    jump = reader.tell()
    to = section.sectionHeader.fixups.get(pointer.ptr)
    if to is not None:
        reader.seek(to)
        func()
    reader.seek(jump)

def classname_of(pointer, section):
    to = section.sectionHeader.fixups.get(pointer.ptr, None)
    if to is None:
        return None
    return section.sectionHeader.virtualFixups.get(to)