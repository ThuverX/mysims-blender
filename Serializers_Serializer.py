from abc import ABC, abstractmethod
from io import BufferedReader, BufferedWriter

class Serializer(ABC):
    @abstractmethod
    def read(self, buf: BufferedReader):
        pass

    @abstractmethod
    def write(self, buf: BufferedWriter):
        pass