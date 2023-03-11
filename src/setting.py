# -*- coding: utf-8 -*-

import json
import pathlib
import traceback

from error import *

class Setting:
    """
    設定管理用のクラス
    """

    def __init__(self, setting_file):
        """
        parameter
            setting_file : 設定ファイルのパス(文字列)
        """
        try:
            path = self.file_check(setting_file)
            self.setting = self.read(path=path)
        except:
            traceback.print_exc()
            self.setting = {}
            return

    def file_check(self, filepath):
        """
        ファイルの正当性をチェックする関数
        
        """
        path = pathlib.Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"\'{filepath}\' is not exist.")
        elif path.suffix != ".json":
            raise InvalidFileExtensionError("suffix is not \'json\'.")

        return path 

    def read(self, path):
        """
        jsonファイルを読み込む

        parameter
            path : pathlib.Pathオブジェクト
        """
        with open(path, mode="r") as f:
            setting = json.load(f)
            return setting
    
    def get(self, key):
        return self.setting[key]
