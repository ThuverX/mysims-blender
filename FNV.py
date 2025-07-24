PRIME_32 = 0x01000193
OFFSET_32 = 0x811C9DC5
PRIME_64 = 0x00000100000001B3
OFFSET_64 = 0xCBF29CE484222325

def fnv32(name: str) -> int:

    hash = OFFSET_32
    for byte in name.lower().encode('utf-8'):
        hash = hash * PRIME_32
        hash ^= byte
    return hash & 0xFFFFFFFF

def fnv64(name: str) -> int:

    hash = OFFSET_64
    for byte in name.lower().encode('utf-8'):
        hash = hash * PRIME_64
        hash ^= byte
    return hash & 0xFFFFFFFFFFFFFFFF