from dataclasses import dataclass, field
from typing import List
from ..BinReader import BinReader
from ..hkCommon import hkPhysicsSystem
from ..hkMacros import array_pointer_foreach
from .hkEntity import hkEntityClass

@dataclass
class hkPhysicsSystemClass:
    hkPhysicsSystem: "hkPhysicsSystem" = field(default_factory=hkPhysicsSystem)
    rigidbodies: List[hkEntityClass] = field(default_factory=list)

    @staticmethod
    def read(obj: "hkPhysicsSystemClass", reader: BinReader, section):
        hkPhysicsSystem.read(obj.hkPhysicsSystem, reader)

        def _each(i: int):
            entity = hkEntityClass()
            hkEntityClass.read(entity, reader, section)
            obj.rigidbodies.append(entity)

        array_pointer_foreach(obj.hkPhysicsSystem.rigidBodies, reader, section, _each)