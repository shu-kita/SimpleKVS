# -*- coding: utf-8 -*-

class Value:
    """
    Key-ValueのValue用のクラス

    バージョン機能の実現のために作成した(3/9)
    古いバージョンを10まで持つようにしている(3/9)

    SimpleKVS側でimportできていない
    """
    
    def __init__(self, value):
        self.value = value
        self.old_values = []
    
    def update(self, new_value):
        """
        valueをアップデートする。
        アップデート前のvalueをold_valuesに格納する

        parameter
            new_value : 更新するvalue
        """

        self.old_values.insert(0, self.value)
        if len(self.old_values) > 10:
            self.old_values = self.old_values[:10]
        
        self.value = new_value
    
    def get_value(self, version=0):
        """
        値を取得する
        指定されたversionよりリストの要素が少ない場合、一番古いバージョンを返す
        指定されたversionが0以下だったら、最新の値を返す

        parameter
            version : 取得するバージョン(初期値は0)
        """
        ret = None

        if version > len(self.old_values):
            ret = self.old_values[-1]
        elif version <= 0:
            ret = self.value
        else:
            self.old_values[version]

        return ret
