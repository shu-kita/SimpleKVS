# -*- coding: utf-8 -*-

"""
サンプルプログラム
動作確認用
"""

from SimpleKVS import *
from Value import *

# 実行用

test_file = "./test.pickle"
kvs = SimpleKVS(test_file)

# kvs.put(1, "test3", True)

value = kvs.get(1)
print(value)

old_value = kvs.get(1, 1)
print(old_value)


"""-----------------------------------------------------------------------------------------------"""

# テスト用データファイル作成

# import pickle

# data = {1: Value("test")}
# print(type(data))

# with open("test.pickle", mode="wb") as f:
#     pickle.dump(data, f)