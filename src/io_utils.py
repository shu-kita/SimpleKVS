# -*- coding: utf-8 -*-

def dump_kv(file_obj, key:str, value:str):
    """
    key, valueを書き込む
    """
    # keyをbyte化、長さの取得
    byte_key = key.encode("utf-8")
    key_len = len(byte_key).to_bytes(4, "little")
    # valueをbyte化、長さの取得
    byte_value = value.encode("utf-8")
    value_len = len(byte_value).to_bytes(4, "little")
    # 書き込むbyte列を生成し、書き込み
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
        # keyの長さを取得
        byte_length = file_obj.read(4)
        if not byte_length:
             break
        # keyを読み込む
        key = read_obj(file_obj, byte_length)
        # valueの長さを取得し、読み込む
        byte_length = file_obj.read(4)
        value = read_obj(file_obj, byte_length)
        yield key.decode(), value.decode()

def dump_index(file_obj, key:str, position:int):
    """
    indexにkey, positionを書き込む
    """
    # keyをbyte化、長さの取得
    byte_key = key.encode("utf-8")
    key_len = len(byte_key).to_bytes(4, "little")
    # positionをbyte化
    position_byte = position.to_bytes(4, "little")
    # 書き込むbyte列を生成し、書き込み
    index = key_len + byte_key + position_byte
    file_obj.write(index)

def load_index(file_obj):
    while True:
        byte_length = file_obj.read(4)
        if not byte_length:
             break
        # keyの長さを取得し、keyを読み込む
        length = int.from_bytes(byte_length,"little")
        key = file_obj.read(length)
        # positionを読み込む
        position = int.from_bytes(file_obj.read(4), "little")
        yield key.decode("utf-8"), position
