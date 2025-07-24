import os
from .FNV import fnv64
from .Serializers_Serializer import Serializer
from .util import *

file_associations = {
    0x01661233: "Model",
    0xf9e50586: "RevoModel",
    0xb359c791: "0xb359c791",
    0x8eaf13de: "rig",
    0x6b20c4f3: "clip",
    0x0166038c: "KeyNameMap",
    0x015a1849: "Geometry",
    0x01d0e75d: "Material",
    0x02019972: "MaterialSet",
    0x00b552ea: "OldSpeedTree",
    0x021d7e8c: "SpeedTree",
    0x00b2d882: "dds",
    0x8e342417: "CompositeTexture",
    0x025ed6f4: "SimOutfit",
    0x585ee310: "LevelXml",
    0x58969018: "LevelBin",
    0xd5988020: "Physics",
    0x50182640: "LightSetXml",
    0x50002128: "LightSetBin",
    0xdc37e964: "xml",
    0x2c81b60a: "FootPrintSet",
    0xc876c85e: "ObjectConstructionXml",
    0xc08ec0ee: "ObjectConstructionBin",
    0x4045d294: "SlotXml",
    0x487bf9e4: "SlotBin",
    0xcf60795e: "swm",
    0x9752e396: "SwarmBin",
    0xe0d83029: "XmlBin",
    0xa6856948: "CABXml",
    0xc644f440: "CABBin",
    0x5bca8c06: "big",
    0xb6b5c271: "bnk",
    0x474999b4: "lua",
    0x2b8e2411: "luo",
    0xb61215e9: "LightBoxXml",
    0xd6215201: "LightBoxBin",
    0x1e1e6516: "xmb",
    0xfd72d418: "ttf",
    0x35ebb959: "ttc",
}

# Reverse mapping for quick lookups from string to int
string_to_int = {v: k for k, v in file_associations.items()}

def typeid_to_typename(value: int) -> str:
    return file_associations.get(value, "Unknown")

def typename_to_id(value: str) -> int:
    return string_to_int.get(value, None)

class ResourceKey(Serializer):
    instance = 0
    type = 0
    group = 0

    def __init__(self, instance = 0, type = 0, group = 0):
        self.instance = instance
        self.type = type
        self.group = group

    def read(self, buf: BufferedReader):
        start_read()
        if get_endianness(buf) == "le":
            self.instance = uint64_t(buf)
            self.type = uint32_t(buf)
            self.group = uint32_t(buf)
        else:
            low = uint32_t(buf)
            high = uint32_t(buf)
            self.instance = low | high << 32
            self.type = uint32_t(buf)
            self.group = uint32_t(buf)

    def write(self, buf: BufferedWriter):
        start_write()

        if get_endianness(buf) == "le":
            uint64_t(buf, self.instance)
        else:
            low = self.instance & 0xFFFFFFFF
            high = (self.instance >> 32) & 0xFFFFFFFF
            uint32_t(buf, low)
            uint32_t(buf, high)

        uint32_t(buf, self.type)
        uint32_t(buf, self.group)

    def __str__(self):
        return f"0x{self.group:08x}!0x{self.instance:016x}.{typeid_to_typename(self.type)}"
    
    def get_extension(self):
        return typeid_to_typename(self.type)

    def __repr__(self):
        return f"<ResourceKey group=0x{self.group:08x}, instance=0x{self.instance:016x}, type=0x{self.type:08x}>"
    
    def __hash__(self):
        return hash((self.instance, self.type, self.group)) 

    def __eq__(self, other):
        return (
            isinstance(other, ResourceKey) and
            self.instance == other.instance and
            self.type == other.type and
            self.group == other.group
        )
    @classmethod
    def from_name(cls, type: int, name: str):
        return cls(fnv64(name), type, 0)
    
    @classmethod
    def from_file_name(cls, path: str):
        try:
            filename = os.path.basename(path)

            if '!' not in filename:
                name_without, extension = os.path.splitext(filename)
                type = typename_to_id(extension[1:])
                instance = fnv64(name_without)

                return cls(instance, type, 0)
            else:
                group_str, rest = filename.split('!')
                instance_str = rest.split('.')[0]
                extension = os.path.splitext(filename)[1]

                group = int(group_str, 16)
                instance = int(instance_str, 16)
                type = typename_to_id(extension[1:])

                return cls(instance, type, group)
        except Exception as e:
            raise ValueError(f"Failed to parse group/instance from: {filename}") from e