# -*- coding: utf-8 -*-
import logging

from pathlib import Path
from io_utils import dump_kv, load_kv

class WAL:
    def __init__(self, path:Path):
        self.path:Path = path
        self.file = open(path, "ab+")
 
    def __del__(self):
        self.file.close()
    
    def set(self, key:str, value:str):
        dump_kv(self.file, key, value)
        self.file.flush()

    def recovery(self):
        logging.info(f"WAL recovery has been executed.")
        self.file.seek(0)
        for k, v in load_kv(self.file):
            yield k, v
    
    def clean_up(self):
        self.file.truncate(0)
        self.file.seek(0)

