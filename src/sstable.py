from pathlib import Path
from datetime import datetime
from io_utils import dump_kv, load_kv, dump_index, load_index

class SSTable:
    def __init__(self, path:Path, memtable:dict={}):
        # 現在時刻(unixtimeで取得)
        
        # sstab_<現在時刻>.datファイルのPathオブジェクトを作成
        self.path = Path(path)
        if self.path.is_dir():
            now = int(datetime.now().timestamp())
            self.path = self.path / f"sstab_{now}.dat"

        self.index_path = self.path.with_name(self.path.name + ".index")
        self.search_index = {}

        if self.path.exists(): # pathが存在する => SSTableを読み込む時
            self.load_search_index()
        elif memtable: # pathが存在しない && memtableが空ではない => sstableに書き込む時
            self.flush_to_sstable(memtable)
        else: # pathが存在しない && memtableが空 => 想定外の処理なのでエラーにする 
            raise ValueError(f"Failed to create SSTable \'{self.path}\'.")

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.path}")'
    
    def __str__(self):
        return self.path.__str__()
    
    def __iter__(self):
        with open(self.path, mode="rb") as sstable:
            for k,v in load_kv(sstable):
                yield k,v

    def flush_to_sstable(self, memtable:dict):
        """
        memtableをsstableに書き込む関数
        """
         # memtableをSStableに書き込む処理
        with open(self.path, mode="ab") as sstable:
            for k,v in sorted(memtable.items()):
                position = sstable.tell()
                dump_kv(sstable, k, v)
                self.search_index[k] = position
        # indexをindexファイルに書き込む処理
        with open(self.index_path, mode="ab") as index_file:
            for k, p in self.search_index.items():
                dump_index(index_file, k, p)

    def load_search_index(self):
        """
        <ファイル名>.dat.indexファイルからindexを読み込む
        """
        with open(self.index_path, mode="rb") as index_file:
            for key, position in load_index(index_file):
                self.search_index[key] = position

    def get(self, key):
        """
        SSTableから、valueを読み込む
        """
        position = self.search_index.get(key) # keyが存在しない場合はNoneが返る        
        if position is None: # keyが存在しない => Noneを返す
            return None
        
        # sstableから、valueを読み込む処理
        with open(self.path, mode="rb") as sstable:
            sstable.seek(position)
            _, v = next(load_kv(sstable))
            return v
    
    def delete(self):
        """
        sstable, indexのファイルを削除する
        """
        self.path.unlink()
        self.index_path.unlink()
    
    @staticmethod
    def compaction(sstable_list):
        merged_table = {}
        for sstable in sstable_list:
            for k,v in sstable:
                merged_table[k] = v

        return merged_table

