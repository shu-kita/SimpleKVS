# -*- coding: utf-8 -*-

import logging
from time import time
from pathlib import Path
from threading import Lock

from sstable import SSTable
from wal import WAL

class SimpleKVS:
    def __init__(self, data_dir:str, memtable_limit:int=1024, compaction_interval=3600):
        logging.info("-----Start init SimpleKVS-----")
        self.lock = Lock()
        
        self.data_dir:Path = Path(data_dir)
        if not self.data_dir.exists(): # data_dirが無い => 作成する
            logging.info(f"Create data directory \'{data_dir}\'")
            self.data_dir.mkdir(parents=True)

        self.memtable:dict = {}
        self.memtable_limit = memtable_limit # memtableに持てるkey-valueの最大値

        self.sstable_list:list[SSTable] = []
        self.load_sstables()
        self.major_compaction()

        self.compaction_interval = compaction_interval
        self.last_compaction_time = time()

        self.wal:WAL = WAL(self.data_dir / "wal")
        self.recovery_wal(self.memtable)

        logging.info("-----Finish init SimpleKVS-----")

    def __getitem__(self, key:str):
        return self.get(key)

    def __contains__(self, key:str):
        return self.get(key) is not None

    def get(self, key:str):
        logging.info(f"get is executed. Key is {key}")
        # memtableから取得
        value = self.memtable.get(key)
        # vがNoneではない = 値が取得できた => returnする
        if value is not None:
            return value if value != "__tombstone__" else None
        
        # SStableから取得(新しいSSTableから順に探す)
        for sstable in reversed(self.sstable_list):
            value = sstable.get(key)
            if value is not None: # vがNoneではない = 値が取得できた => returnする
                return value if value != "__tombstone__" else None
        # memtable, SSTableともにない -> Noneをreturnする
        
        logging.info(f"Key \'{key}\' is not found.")
        return None
    
    def set(self, key:str, value:str):
        if value != "__tombstone__":
            logging.info(f"set is executed. key is {key} and value is {value}")

        with self.lock:
            self.wal.set(key, value)
            self.memtable[key] = value
            # memtableのサイズがlimitを超えたとき
            if len(self.memtable) >= self.memtable_limit:
                sstable = SSTable(self.data_dir, self.memtable)
                self.sstable_list.append(sstable)
                self.memtable = {}
                self.wal.clean_up()
        
            interval = time() - self.last_compaction_time
            if interval >= self.compaction_interval:
                self.minor_compaction()

    def delete(self, key:str):
        logging.info(f"delete is executed. Key is {key}")
        # tombstoneをsetする。
        # 実際に削除されるのはcompaction実行時
        if key in self.memtable:
            self.set(key, "__tombstone__")

    def recovery_wal(self, memtable:dict):
        for key,value in self.wal.recovery():
            memtable[key] = value
    
    def load_sstables(self):
        logging.info("Starting To load SSTables.")
        num = 0
        for sstable in sorted(self.data_dir.glob("sstab_*.dat")):
            self.sstable_list.append(SSTable(sstable))
            num += 1
        
        logging.info(f"{num} SSTables is loaded.")
        
    def major_compaction(self):
        logging.info("Starting Major Compaction.")
        # SSTableの数が1以下(2より下)のとき、compactionしない
        number_of_sstables = len(self.sstable_list)
        if number_of_sstables < 2:
            logging.info("Number of SSTable is less than 2")
            return
        
        # compaction処理
        sstable_list_copy = self.sstable_list[:]
        merged_memtable = {}
        # 古いSSTableをreadして、memtableに格納する
        for sstable in self.sstable_list:
            for key,value in sstable:
                merged_memtable[key] = value
                # valueがtombstoneの時 -> keyを削除する
                if value == "__tombstone__":
                    del merged_memtable[key]
        # mergeし、1つになったmemtableをSSTableに書き込む
        merged_sstable = SSTable(self.data_dir, merged_memtable)
        
        self.sstable_list = [merged_sstable]

        # 古いsstableの削除
        for old_sstable in sstable_list_copy:
            old_sstable.delete()

        logging.info(f"The number of SSTables has decreased from {number_of_sstables} to 1.")

    def minor_compaction(self):
        logging.info("Starting Minor Compaction.")
        # SSTableの数が1以下(2より下)のとき、compactionしない
        if len(self.sstable_list) < 2:
            logging.info("Number of SSTable is less than 2")
            return

        merged_memtable = {}
        # 古いSSTableから順にdictに格納する
        # SSTableは削除する。
        sstables = self.sstable_list[:2] # compaction対象のSSTableを取得(リストの先頭2個)
        for sstable in sstables:
            for key, value in sstable:
                merged_memtable[key] = value
            # SSTableのパスを取得
            path = sstables[1].path
            self.sstable_list.remove(sstable)
            sstable.delete()
        # 再作成し、リストの先頭に入れる
        # (一・二番目に古いSSTableをCompactionする前提。)
        self.sstable_list.insert(0, SSTable(path, merged_memtable))
        self.last_compaction_time = time()