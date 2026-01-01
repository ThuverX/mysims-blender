from dataclasses import dataclass, field
from typing import List
from ..BinReader import BinReader
from ..hkCommon import hkPhysicsData
from ..hkMacros import array_pointer_foreach
from .hkPhysicsSystem import hkPhysicsSystemClass

@dataclass
class hkPhysicsDataClass:
    hkPhysicsData: "hkPhysicsData" = field(default_factory=hkPhysicsData)
    systems: List[hkPhysicsSystemClass] = field(default_factory=list)

    @staticmethod
    def read(obj: "hkPhysicsDataClass", reader: BinReader, section):
        hkPhysicsData.read(obj.hkPhysicsData, reader)

        def _each(i: int):
            system = hkPhysicsSystemClass()
            hkPhysicsSystemClass.read(system, reader, section)
            obj.systems.append(system)

        array_pointer_foreach(obj.hkPhysicsData.systemsArray, reader, section, _each)