# -*- coding: utf-8 -*-

def dump_kv(file_obj, key, value):
    """
    key, valueを書き込む
    """
    byte_key = key.encode("utf-8")
    key_len = len(byte_key).to_bytes(4, "little")
    byte_value = value.encode("utf-8")
    value_len = len(byte_value).to_bytes(4, "little")
    key_value_pair = key_len + byte_key + value_len + byte_value

    file_obj.write(key_value_pair)
 

def load_kv(file_obj):
    """
    key,valueを読み込む
    """

    def read_obj(file, byte_length):
        """
        byte→intに変換し、keyかvalueの長さを取得
        取得した長さ分fileからReadする
        """
        length = int.from_bytes(byte_length,"little")
        return file.read(length)

    while True:
        byte_length = file_obj.read(4)
        if not byte_length:
             break
        key = read_obj(file_obj, byte_length)
        byte_length = file_obj.read(4)
        value = read_obj(file_obj, byte_length)
        yield key.decode(), value.decode()

def dump_index(file_obj, key:str, position:int):
    """
    indexにkey, positionを書き込む
    """
    byte_key = key.encode("utf-8")
    key_len = len(byte_key).to_bytes(4, "little")
    positon_byte = position.to_bytes(4, "little")
    index = key_len + byte_key + positon_byte
    file_obj.write(index)

def load_index(file_obj):
    while True:
        byte_length = file_obj.read(4)
        if not byte_length:
             break
        length = int.from_bytes(byte_length,"little")
        key = file_obj.read(length)
        position = int.from_bytes(file_obj(4), "little")
        yield key.decode("utf-8"), position

f = open("test.dat", mode="rb")
print(f.tell())
f.read(4)
print(f.tell())
f.close()