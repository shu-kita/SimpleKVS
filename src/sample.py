# -*- coding: utf-8 -*-

"""
サンプルプログラム
動作確認用
"""

from skvs import *
from value import *

# 実行用

# test_file = "./test.pickle"
kvs = SimpleKvs()

# # kvs.put(1, "test3", True)

# value = kvs.get("1")
# print(value)

# kvs.put("2", "test2")

# kvs.scan()

"""-----------------------------------------------------------------------------------------------"""

# テスト用データファイル作成
# False -> Trueに変更して使用
if False:
    v = Value("test")
    s = v.serialize()
    test_data = {
        "1": s
    }

    with open("test.pack", mode="wb") as f:
        f.write(msgpack.packb(test_data))


"""-----------------------------------------------------------------------------------------------"""

# 設定ファイル作成用

# jsondata = {"data_file": "test.pickle"}

# file = "setting.json"
# with open(file, mode="w") as f:
#     json.dump(jsondata, f)