from pathlib import Path
from threading import Lock

from sstable import SSTable
from wal import WAL

class SimpleKVS:
    def __init__(self, data_dir, memtable_limit=1024):
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists(): # data_dirが無い => 作成する
            self.data_dir.mkdir(parents=True)

        self.memtable = {}
        self.memtable_limit = memtable_limit # memtableに持てるkey-valueの最大値

        self.sstable_list = []
        self.load_sstables()
        self.marge_sstables()

        self.wal = WAL(self.data_dir / "wal")
        self.recovery_wal(self.memtable)

    def __getitem__(self, key):
        return self.get(key)


    def __contains__(self, key):
        return self.get(key) is not None

    def get(self, key):
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
    
    def set(self, key, value):
        with Lock():
            self.wal.set(key, value)
            self.memtable[key] = value
            # memtableのサイズがlimitを超えたとき
            if len(self.memtable) >= self.memtable_limit:
                sstable = SSTable(self.data_dir, self.memtable)
                self.sstable_list.append(sstable)
                self.memtable = {}
                self.wal.clean_up()

    def recovery_wal(self, memtable):
        for k,v in self.wal.recovery():
            memtable[k] = v
    
    def load_sstables(self):
        for sstable in self.data_dir.glob("sstab_*.dat"):
            self.sstable_list.append(SSTable(sstable))
        
    def marge_sstables(self):
        if len(self.sstable_list) < 2:
            return
        
        # compaction実行
        copy_list = self.sstable_list[:]
        marged_table = SSTable.compaction(self.sstable_list)
        sstable = SSTable(self.data_dir, marged_table)
        
        self.sstable_list = [sstable]

        # 古いsstableの削除
        for table in copy_list:
            table.delete()
