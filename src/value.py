# -*- coding: utf-8 -*-

import logging
from collections import deque

class Value:
    """
    Key-ValueのValue用のクラス
    """

    def __init__(self, value):
        self.values = deque([value])
    
    def update(self, new_value):
        """
        new_valueをvaluesリストの先頭に挿入する。

        parameter
            new_value : 更新するvalue
        """
        self.values.appendleft(new_value)

    def get_value(self, version=0):
        """
        値を取得する
        version > リストの要素数 の場合、一番古いバージョンを返し、
        version <= 0 の場合、最新の値を返す

        parameter
            version : 取得するバージョン(初期値は0)
        """
        ret = None

        if version > len(self.values):
            ret = self.values[-1]
            logging.warning(f"Unexpected value of version ({version}). Please provide a value between 1 and 10. Returning oldest version.")
        elif version <= 0:
            ret = self.values[0]
            logging.warning(f"Unexpected value of version ({version}). Please provide a value between 1 and 10. Returning latest version.")
        else:
            ret = self.values[version]

        return ret
    
    def get_latest(self):
        """
        最新バージョンを返す関数
        """
        return self.values[0]
    
