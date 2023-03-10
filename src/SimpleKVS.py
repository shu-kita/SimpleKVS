# -*- coding: utf-8 -*-

import pickle
from Value import *

class SimpleKVS:
    
    def __init__(self, pickle_file):
        self.db = {}
        self.pickle_file = pickle_file
        try:
            with open(pickle_file, 'rb') as f:
                self.db = pickle.load(f)
        except FileNotFoundError:
            return

    def __del__(self):
        self.save()

    def is_exist(self):
        """
        ファイルの存在をチェックする

        parameter
            無し
        """
        result = True
        if not self.db:
            print(f"{self.pickle_file} is not exist.")
            result = False
        
        return result
        
    def put(self, key, value, is_overwrite=False):
        """
        parameter
            key : キー
            value : 値
            is_overwrite : 上書きする/しない(True=する, False=しない)
        """
        if not self.is_exist():
            return

        if key not in self.db:
            v = Value(value)
            self.db[key] = v
        elif is_overwrite:
            v = self.db[key]
            v.update(value)
            self.db[key] = v
        else:
            print(f"Key '{key}' is already exist.")

    def get(self, key, version=0):
        """
        キーを指定し、バリューを取得する

        parameter
            key : キー
            version : valueのバージョン指定する(デフォルト0)
        """
        if not self.is_exist():
            return
        
        if key in self.db:
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
        if not self.is_exist():
            return
        
        for key, value in self.db.items():
            print(f"{key}: {value.value}")

    def delete(self, key):
        """
        キーを指定し、バリューを削除する

        parameter
            key : キー
        """
        if not self.is_exist():
            return
        
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
        with open(self.pickle_file, 'wb') as f:
            pickle.dump(self.db, f)
