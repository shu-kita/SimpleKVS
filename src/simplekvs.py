# -*- coding: utf-8 -*-

from pathlib import Path
from threading import Lock

from sstable import SSTable
from wal import WAL

class SimpleKVS:
    def __init__(self, data_dir:str, memtable_limit=1024):
        self.data_dir:Path = Path(data_dir)
        if not self.data_dir.exists(): # data_dirが無い => 作成する
            self.data_dir.mkdir(parents=True)

        self.memtable:dict = {}
        self.memtable_limit:int = memtable_limit # memtableに持てるkey-valueの最大値

        self.sstable_list:list[SSTable] = []
        self.load_sstables()
        self.compaction()

        self.wal:WAL = WAL(self.data_dir / "wal")
        self.recovery_wal(self.memtable)

    def __getitem__(self, key:str):
        return self.get(key)

    def __contains__(self, key:str):
        return self.get(key) is not None

    def get(self, key:str):
        # memtableから取得
        v = self.memtable.get(key)
        if v is not None: # vがNoneではない = 値が取得できた => returnする
            return v
        
        # SStableから取得(新しいSSTableから順に探す)
        for sstable in reversed(self.sstable_list):
            v = sstable.get(key)
            if v is not None: # vがNoneではない = 値が取得できた => returnする
                return v
        # memtable, SSTableともにない => Noneをreturn
        return
    
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
        """
        TODO
            * memtableの削除しかしていない
              SSTable側にキーがあれば、あるということになるし、Compaction時に復活する
              -> Deleteできていない
        """
        del self.memtable[key]

    def recovery_wal(self, memtable:dict):
        for k,v in self.wal.recovery():
            memtable[k] = v
    
    def load_sstables(self):
        for sstable in self.data_dir.glob("sstab_*.dat"):
            self.sstable_list.append(SSTable(sstable))
        
    def compaction(self):
        # SSTableの数が1以下(2より下)のとき、compactionしない
        if len(self.sstable_list) < 2:
            return
        
        # compaction処理
        copy_list = self.sstable_list[:]

        merged_table = {}
        for sstable in self.sstable_list:
            for k,v in sstable:
                merged_table[k] = v
        merged_sstable = SSTable(self.data_dir, merged_table)
        
        self.sstable_list = [merged_sstable]

        # 古いsstableの削除
        for old_sstable in copy_list:
            old_sstable.delete()
