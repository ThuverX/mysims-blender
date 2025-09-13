import bpy
import struct
from typing import Literal, Any, Callable
from io import BufferedReader, BufferedWriter

ENDIANNESS = Literal["le", "be"]
BUFFER_ENDIANNESS: dict[Any, ENDIANNESS] = {}


def set_endianness(buf, endianness: ENDIANNESS):
    BUFFER_ENDIANNESS[buf] = endianness


def get_endianness(buf) -> ENDIANNESS:
    return BUFFER_ENDIANNESS.get(buf) or "le"


def get_endianness_char(buf):
    if get_endianness(buf) == "le":
        return "<"
    else:
        return ">"


mode = "read"


def start_read():
    global mode
    mode = "read"


def start_write():
    global mode
    mode = "write"


def offset(buf) -> int:
    return buf.tell()


def seek(buf, value):
    buf.seek(value)


def uint64_t(buf, value=None) -> int:
    if mode == "read":
        return struct.unpack(get_endianness_char(buf) + "Q", buf.read(8))[0]
    else:
        buf.write(struct.pack(get_endianness_char(buf) + "Q", value))


def uint32_t(buf, value=None) -> int:
    if mode == "read":
        return struct.unpack(get_endianness_char(buf) + "I", buf.read(4))[0]
    else:
        buf.write(struct.pack(get_endianness_char(buf) + "I", value))


def float32_t(buf, value=None) -> float:
    if mode == "read":
        return struct.unpack(get_endianness_char(buf) + "f", buf.read(4))[0]
    else:
        buf.write(struct.pack(get_endianness_char(buf) + "f", value))


def uint16_t(buf, value=None) -> int:
    if mode == "read":
        return struct.unpack(get_endianness_char(buf) + "H", buf.read(2))[0]
    else:
        buf.write(struct.pack(get_endianness_char(buf) + "H", value))


def uint8_t(buf, value=None) -> int:
    if mode == "read":
        return struct.unpack(get_endianness_char(buf) + "B", buf.read(1))[0]
    else:
        buf.write(struct.pack(get_endianness_char(buf) + "B", value))


def char(buf, value=None) -> str:
    if mode == "read":
        return struct.unpack(get_endianness_char(buf) + "c", buf.read(1))[0].decode()
    else:
        buf.write(struct.pack(get_endianness_char(buf) + "c", value.encode()))


def string(buf, size=None, value=None) -> str:
    if mode == "read":
        return buf.read(size).decode()
    else:
        buf.write(value.encode().ljust(size, b'\x00'))


def sized_string(buf, value=None) -> str:
    if mode == "read":
        size = uint32_t(buf)
        return string(buf, size)
    else:
        encoded = value.encode()
        uint32_t(buf, len(encoded))
        buf.write(encoded)


def cstring(buf, value=None) -> str:
    if mode == "read":
        result = bytearray()
        c = uint8_t(buf)
        while c != 0:
            result.append(c)
            c = uint8_t(buf)
        out = result.decode()
        if get_endianness(buf) == "be":
            return out[::-1]
        return out
    else:
        if get_endianness(buf) == "be":
            value = value[::-1]
        buf.write(value.encode('utf-8') + b'\x00')


def skip(buf, size=1):
    if mode == "read":
        buf.read(size)
    else:
        buf.write(b'\x00' * size)

def get_game_path():
    scene = bpy.context.scene
    scene_props = scene.mysims_data

    if scene_props and scene_props.game_path:
        return scene_props.game_path
    return None


class Vector3:
    x = 0.0
    y = 0.0
    z = 0.0
    mode = "MYSIMS"

    def __init__(self, x=0.0, y=0.0, z=0.0, mode="MYSIMS"):
        self.x = x
        self.y = y
        self.z = z
        self.mode = mode

    def read(self, buf: BufferedReader):
        self.x = float32_t(buf)
        self.y = float32_t(buf)
        self.z = float32_t(buf)

    def write(self, buf: BufferedWriter):
        float32_t(buf, self.x)
        float32_t(buf, self.y)
        float32_t(buf, self.z)

    def as_blender(self):
        if self.mode == "BLENDER":
            return Vector3(self.x, self.y, self.z, mode="BLENDER")

        blender_vec = Vector3(
            -self.x,
            self.z,
            self.y,
            mode="BLENDER"
        )
        return blender_vec

    def as_mysims(self):
        if self.mode == "MYSIMS":
            return Vector3(self.x, self.y, self.z, mode="MYSIMS")

        mysims_vec = Vector3(
            -self.x,
            self.z,
            self.y,
            mode="MYSIMS"
        )
        return mysims_vec

    def min(self, other):
        local_left = self.as_blender()
        local_right = other.as_blender()
        return Vector3(min(local_left.x, local_right.x), min(local_left.y, local_right.y),
                       min(local_left.z, local_right.z), mode="BLENDER")

    def max(self, other):
        local_left = self.as_blender()
        local_right = other.as_blender()
        return Vector3(max(local_left.x, local_right.x), max(local_left.y, local_right.y),
                       max(local_left.z, local_right.z), mode="BLENDER")


class Vector2:
    x = 0.0
    y = 0.0

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def read(self, buf: BufferedReader):
        start_read()
        self.x = float32_t(buf)
        self.y = float32_t(buf)

    def write(self, buf: BufferedWriter):
        start_write()
        float32_t(buf, self.x)
        float32_t(buf, self.y)
