import os
from io import BufferedReader
import bpy
from .Serializers.ResourceKey import ResourceKey
from .util import get_game_path
from contextlib import nullcontext

class MySimsFileSystem:
    records: dict[ResourceKey, str]
    ready: bool

    def __init__(self):
        self.ready = False

    def update(self):
        self.records = {}
        self.records.clear()
        self.ready = False

        bpy.context.window.cursor_set('WAIT')

        itr = 0
        root_path = get_game_path()
        for dirpath, folders, files in os.walk(root_path):
            for filepath in files:
                # TODO: if extension is .package, load using DBPF
                file_key = ResourceKey.from_file_name(filepath)
                self.records[file_key] = os.path.join(dirpath, filepath)
                itr += 1

        print("Loaded {0} records".format(itr))
        self.ready = True
        bpy.context.window.cursor_set('DEFAULT')

    def get(self, key: ResourceKey) -> str | None:
        if not self.ready:
            self.update()
            if not self.ready:
                pass # We somehow still didn't initialize
        return self.records.get(key) or None

    def open(self, key: ResourceKey) -> BufferedReader | type[nullcontext]:
        path = self.get(key)
        if path:
            return open(path, 'rb')

        return nullcontext

    def exists(self, key: ResourceKey) -> bool:
        if not self.ready:
            self.update()
            if not self.ready:
                pass # We somehow still didn't initialize
        return self.get(key) is not None

MS_FILE_SYSTEM: MySimsFileSystem = MySimsFileSystem()