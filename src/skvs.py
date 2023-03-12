# -*- coding: utf-8 -*-

import pickle
import traceback
import msgpack
from value import *
from setting import *

class SimpleKvs:
    
    def __init__(self):
        self.db = {}
        try:
            self.setting = Setting("setting.json") # 設定ファイルからSettingオブジェクトを作成
            data_file = self.setting.get("data_file")
            print(data_file)
            with open(data_file, 'rb') as f:
                bin_data = f.read()
                unpack_data = msgpack.unpackb(bin_data)
                for k,v in unpack_data.items():
                    self.db[k] = pickle.loads(v)
        except:
            traceback.print_exc()
            return

    def __del__(self):
        self.save()

    def put(self, key, value, is_overwrite=False):
        """
        parameter
            key : キー
            value : 値
            is_overwrite : 上書きする/しない(True=する, False=しない)
        """
        if not self.contains_key(key): # DBにkeyが無いとき(新規作成)の処理
            v = Value(value)
            self.db[key] = v
        elif is_overwrite: # 上書きのときの処理
            v = self.db[key]
            v.update(value)
            self.db[key] = v
        else: # Keyが存在していて、上書きモードではない時の処理
            print(f"Key '{key}' is already exist.")

    def get(self, key, version=0):
        """
        キーを指定し、バリューを取得する

        parameter
            key : キー
            version : valueのバージョン指定する(デフォルト0)
        """
        if self.contains_key(key):
            value = self.db[key]
            return value.get_value(version)
        else:
            return None

    def scan(self):
        """
        全件表示する

        parameter
            無し
        """
        for key, value in self.db.items():
            print(f"{key}: {value.values[0]}")

    def delete(self, key):
        """
        キーを指定し、バリューを削除する

        parameter
            key : キー
        """
        if key in self.db:
            del self.db[key]
        else:
            print(f"Key '{key}' is not exist.")

    def save(self):
        """
        現在のデータで保存する

        parameter
            無し
        """
        data_file = self.setting.get("data_file")
        with open(data_file, mode='wb') as f:
            tmp_db = self.db.copy() # 参照写しにより、self.dbのvalueがシリアライズされないためコピー
            for k,v in tmp_db.items():
                tmp_db[k] = v.serialize()
            pack = msgpack.packb(tmp_db)
            f.write(pack)

            
    def contains_key(self, key):
        """
        Keyの存在を確認する処理

        parameter
            key : キー
        
        return
            boolean
        """
        return key in self.db
