# Python port of the provided Havok reader headers.

Top-level reader:
- HavokFile.py provides HavokFileReader(Serializer) which reads the whole file.

Usage:
```
    from io import BufferedReader
    from HavokFile import HavokFileReader

    with open('file.hkxpack', 'rb') as f:
        reader = HavokFileReader()
        result = reader.read(f)  # result is HavokFile dataclass
```