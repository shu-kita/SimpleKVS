# -*- coding: utf-8 -*-

from pathlib import Path
from threading import Lock

from sstable import SSTable
from wal import WAL

class SimpleKVS:
    def __init__(self, data_dir:str, memtable_limit:int=1024):
        self.data_dir:Path = Path(data_dir)
        if not self.data_dir.exists(): # data_dirが無い => 作成する
            self.data_dir.mkdir(parents=True)

        self.memtable:dict = {}
        self.memtable_limit = memtable_limit # memtableに持てるkey-valueの最大値

        self.sstable_list:list[SSTable] = []
        self.load_sstables()
        self.major_compaction()

        self.wal:WAL = WAL(self.data_dir / "wal")
        self.recovery_wal(self.memtable)

    def __getitem__(self, key:str):
        return self.get(key)

    def __contains__(self, key:str):
        return self.get(key) is not None

    def get(self, key:str):
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
        return None
    
    def set(self, key:str, value:str):
        with Lock():
            self.wal.set(key, value)
            self.memtable[key] = value
            # memtableのサイズがlimitを超えたとき
            if len(self.memtable) >= self.memtable_limit:
                sstable = SSTable(self.data_dir, self.memtable)
                self.sstable_list.append(sstable)
                self.memtable = {}
                self.wal.clean_up()
    
    def delete(self, key:str):
        if key in self.memtable:
            self.set(key, "__tombstone__")


    def recovery_wal(self, memtable:dict):
        for key,value in self.wal.recovery():
            memtable[key] = value
    
    def load_sstables(self):
        for sstable in self.data_dir.glob("sstab_*.dat"):
            self.sstable_list.append(SSTable(sstable))
        
    def major_compaction(self):
        # SSTableの数が1以下(2より下)のとき、compactionしない
        if len(self.sstable_list) < 2:
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

    def minor_compaction(sstables:list[SSTable, SSTable]):
        merged_memtable = {}
        # 古いSSTableから順にdictに格納する
        # SSTableは削除する。
        # (呼び出し側で、順番を意識する)
        for sstable in sstables:
            for key, value in sstable:
                merged_memtable[key] = value
            sstable.delete()

        # memtableを2つのSSTableの新しい方と同名のファイルを、
        # Compaction後のSSTableとして再作成する。    
        path = sstables[1].path
        SSTable(path, merged_memtable)