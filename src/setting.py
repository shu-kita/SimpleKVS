# -*- coding: utf-8 -*-

import json
import pathlib

from error import *

class Setting:
    """
    設定管理用のクラス
    """

    def __init__(self, setting_file):
        """
        コンストラクタ(初期化処理)
        設定ファイル(json)を読み込む
        ファイルが存在しない時、jsonファイル(拡張子が.json)ではない時、例外をあげる

        parameter
            setting_file : 設定ファイルのパス(文字列)
        """
        path = pathlib.Path(setting_file)
        if not path.exists:
            raise SettingFileNotFoundError(f"The setting file that name is \'{setting_file}\' can not find.")
        elif path.suffix != ".json":
            raise InvalidFileExtensionError("suffix is not \'json\'.")

        self.setting = self.read(path=path)
        return

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
        """
        指定されたkeyに対するvalueを返す

        parameter
            key : キー
        """
        if key in self.setting.keys():
            value = self.setting[key]
        else:
            value = None
        
        return value
