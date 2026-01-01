import struct
from io import BufferedReader
from typing import BinaryIO

class BinReader:
    def __init__(self, buf: BinaryIO, little_endian: bool = True):
        # Wrap any binary stream which supports read/seek/tell
        self.buf = buf
        self.little_endian = little_endian
        # determine size without disturbing current position
        pos = self.buf.tell()
        self.buf.seek(0, 2)
        self._size = self.buf.tell()
        self.buf.seek(pos, 0)

    def tell(self) -> int:
        return self.buf.tell()

    def size(self) -> int:
        return self._size

    def seek(self, offset: int, whence: int = 0):
        self.buf.seek(offset, whence)

    def skip(self, n: int):
        if n:
            self.buf.seek(self.buf.tell() + n, 0)

    def read_bytes(self, n: int) -> bytes:
        data = self.buf.read(n)
        if len(data) != n:
            raise EOFError("Unexpected EOF")
        return data

    def read_cstring(self) -> str:
        # read until null byte
        chars = bytearray()
        while True:
            b = self.read_bytes(1)
            if b == b'\x00':
                break
            chars.extend(b)
        return chars.decode('utf-8', errors='ignore')

    def _unpack(self, fmt: str, nbytes: int):
        data = self.read_bytes(nbytes)
        return struct.unpack(('<' if self.little_endian else '>') + fmt, data)[0]

    def read_u8(self) -> int:
        return self._unpack('B', 1)

    def read_u16(self) -> int:
        return self._unpack('H', 2)

    def read_u32(self) -> int:
        return self._unpack('I', 4)

    def read_u64(self) -> int:
        return self._unpack('Q', 8)

    def read_f32(self) -> float:
        return self._unpack('f', 4)