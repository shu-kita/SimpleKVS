# -*- coding: utf-8 -*-

"""
サンプルプログラム
動作確認用
"""

from skvs import *
from value import *

# 実行用

test_file = "./test.pickle"
kvs = SimpleKVS()

# kvs.put(1, "test3", True)

value = kvs.get(1)
print(value)

value2 = kvs.get(1, version=1)
print(value2)


"""-----------------------------------------------------------------------------------------------"""

# テスト用データファイル作成

# import pickle

# data = {1: Value("test")}
# print(type(data))

# with open("test.pickle", mode="wb") as f:
#     pickle.dump(data, f)

# pickleファイルの中を確認

# with open("test.pickle", mode="rb") as f:
#     obj = pickle.load(f)
#     print(obj[1].values)

"""-----------------------------------------------------------------------------------------------"""

# 設定ファイル作成用

# jsondata = {"data_file": "test.pickle"}

# file = "setting.json"
# with open(file, mode="w") as f:
#     json.dump(jsondata, f)