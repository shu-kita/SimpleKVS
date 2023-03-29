from pathlib import Path
from io_utils import load_index

class SSTable:
    def __init__(self, path:str):
        self.path = Path(path)
        self.index_file = Path(path + ".index")
        self.search_index = {}

        self.path

    def load_search_index(self):
        with open(self.index_file, mode="rb") as index_file:
            for key, position in load_index(index_file):
                self.search_index[key] = position


SSTable("test.dat")