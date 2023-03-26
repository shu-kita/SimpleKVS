# -*- coding: utf-8 -*-

import atexit
import logging
import pathlib
import pickle
import traceback
import msgpack
from error import SettingFileNotFoundError, InvalidFileExtensionError
from value import *
from setting import *

class SimpleKvs:
    def __init__(self):
        self.db = {}
        try:
            setting_file = "setting.json"
            self.setting = Setting(setting_file=setting_file)
            log_file = self.setting.get("log_file")

            # ログファイル、フォーマット指定
            logging.basicConfig(
                filename=log_file,
                format='%(asctime)s [%(levelname)s] %(message)s',
                level=logging.INFO,
                encoding="utf-8"
                )
            logging.info("Starting SimpleKVS...")

            # データファイル取得
            data_file = self.setting.get("data_file")
            logging.info(f"Using datafile : {data_file}")

            # valueの保存するバージョン数を取得
            self.max_version = self.setting.get("max_version")
            if self.max_version is None:
                self.max_version = 10
                logging.warn(f"Can not find key \'max_varsion\' in {setting_file}. Default max version is 10.")

            # データのロード
            self.db = self.load_db(data_file)
            logging.info(f"SimpleKVS started successfully.")

            # プログラム終了時にseveを実行するための処理
            atexit.register(self.save)

        # 設定ファイルが見つからない or 拡張子が.jsonではない時の処理
        # 設定ファイルが読めず、ログファイルが決まらないため、コンソールに出す
        except (SettingFileNotFoundError,InvalidFileExtensionError):
            logging.basicConfig(
                format='%(asctime)s [%(levelname)s] %(message)s',
                level=logging.INFO,
                encoding="utf-8"
            )
            logging.error(traceback.format_exc())

        # 設定ファイルが見つからない時以外の処理。ログファイルに出力する
        except:
            message = f"SimpleKVS failed to start due to the following error :\n{traceback.format_exc()}"
            logging.error(msg=message)

    def load_db(self, data_file):
        """
        データファイル(データベース)からデータをロードする関数

        parameter
            data_file : データファイルのファイル名
        """
        path = pathlib.Path(data_file)
        if path.exists():
            with open(data_file, 'rb') as f:
                binary = f.read()
                unpack = msgpack.unpackb(binary)
                obj = {}
                for k,v in unpack.items():
                    obj[k] = pickle.loads(v)
            return obj
        else:
            raise FileNotFoundError(f"{data_file} is not found.")

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

            # 現在のバージョン数とmax_versionを比較し、多かったら古いバージョンを消す
            num_versions = len(v.values)
            if num_versions >= self.max_version:
                v.values.pop()
                logging.info(f"Value of key \'{key}\''s version exceed max_version. Removing oldest version.")

            v.update(value)
            self.db[key] = v
        else: # Keyが存在していて、上書きモードではない時の処理
            logging.warn(f"put('{value}') is executed, but Key '{key}' is already exist.")
            raise KeyError(f"Key '{key}' already exists in the database and is_overwrite is set to False.")

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
            logging.warn(f"get('{key}') is executed, but key '{key}' is not exist.")
            return None

    def scan(self):
        """
        全件表示する

        parameter
            無し
        """
        for key, value in self.db.items():
            print(f"{key}: {value.get_latest()}")
            
    def delete(self, key):
        """
        キーを指定し、バリューを削除する

        parameter
            key : キー
        """
        if key in self.db:
            del self.db[key]
        else:
            logging.warn(f"delete('{key}') is executed, but key '{key}' is not exist.")
            raise KeyError(f"Key '{key}' already exists in the database and is_overwrite is set to False.")

    def save(self):
        """
        現在のデータで保存する

        parameter
            無し
        """
        data_file = self.setting.get("data_file")
        with open(data_file, mode='wb') as f:
            tmp_db = self.db.copy() # 参照写しにより、self.dbのvalueがpickle.dumpsされないためコピー
            for k,v in tmp_db.items():
                tmp_db[k] = pickle.dumps(v)
            pack = msgpack.packb(tmp_db)
            f.write(pack)

    def contains_key(self, key):
        """
        Keyの存在を確認する処理
        データを複数ファイルに分けるとかやりだすと、特殊な処理が必要な気がするので、一応関数にしている

        parameter
            key : キー
        
        return
            boolean
        """
        return key in self.db.keys()
