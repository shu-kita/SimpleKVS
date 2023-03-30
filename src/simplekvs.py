from pathlib import Path
from sstable import SSTable
from wal import WAL

class SimpleKVS:
    def __init__(self, data_dir, memtable_limit=1024):
        self.data_dir = Path(data_dir)
        if self.data_dir.exists(): # data_dirが無い => 作成する
            self.data_dir.mkdir(parents=True)

        self.memtable = {}
        self.memtable_limit = memtable_limit # memtableに持てるkey-valueの最大値

        self.sstable_list = []
        self.load_sstables()

        self.wal = WAL(self.data_dir / "wal")
        self.recovery_wal(self.memtable)

    def recovery_wal(self, memtable):
        for k,v in self.wal.recovery():
            memtable[k] = v
    
    def load_sstables(self):
        for sstable in self.data_dir.glob("sstab_*.dat"):
            self.sstable_list.add(SSTable(sstable))
        # 最新のSSTableが先頭に来るように
        self.sstable_list.reverse()
        
