# -*- coding: utf-8 -*-

import pickle

class Value:
    """
    Key-ValueのValue用のクラス

    バージョン機能の実現のために作成した(3/9)
    古いバージョンを10まで持つようにしている(3/9)

    現状、リストでいいと思うが、機能を増やす場合にクラス化したほうがよさそうな気がしている
    """
    
    def __init__(self, value):
        self.values = [value]
    
    def update(self, new_value):
        """
        valueをアップデートする。
        アップデート前のvalueをold_valuesに格納する

        parameter
            new_value : 更新するvalue
        """
        self.values.insert(0, new_value)
        if len(self.values) > 10:
            self.values = self.values[:10]        
    
    def get_value(self, version=0):
        """
        値を取得する
        指定されたversionよりリストの要素が少ない場合、一番古いバージョンを返す
        指定されたversionが0以下だったら、最新の値を返す

        parameter
            version : 取得するバージョン(初期値は0)
        """
        ret = None

        if version > len(self.values):
            ret = self.values[-1]
        elif version <= 0:
            ret = self.values[0]
        else:
            ret = self.values[version]

        return ret

    def serialize(self):
        """
        自身をシリアライズ化するメソッド
        """
        return pickle.dumps(self)