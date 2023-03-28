# -*- coding: utf-8 -*-

from struct import pack, unpack
from pathlib import Path


def dump_kv(file, key, value):
    """
    key, valueを書き込む
    """
    byte_key = key.encode("utf-8")
    key_len = pack("I", len(byte_key))
    byte_value = value.encode("utf-8")
    value_len = pack("I", len(byte_value))
    all = key_len + byte_key + value_len + byte_value

    file.write(all)
 

def load_kv(file_obj):
    """
    key,valueを読み込む
    """

    def read(file, byte_length):
        """
        unpackし、key or valueの長さを取得
        取得した長さ分fileからReadする
        """
        length = unpack("I", byte_length)[0]
        return file.read(length)

    while True:
        byte_length = file_obj.read(4)
        if not byte_length:
             break
        key = read(file_obj, byte_length)
        byte_length = file_obj.read(4)
        value = read(file_obj, byte_length)
        yield key.decode(), value.decode()

d = dict()

p = Path("test.dat")
f = open(p, mode="rb")
for k,v in load_kv(file_obj=f):
    print(k, v)
    d[k] = v

d["00000"] = "daigo"
d["0"] = "daigo"
print(dict(sorted(d.items())))


f.close()
# dump_kv(p, "00001", "kitamura")
# dump_kv(p, "00002", "shusei")


if False:
    path = "test.txt"
    file = open(path, mode="r")
    file.seek(2)
    txt = file.read(4)
    print(txt)
    file.close()


