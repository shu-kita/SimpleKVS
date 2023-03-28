# -*- coding: utf-8 -*-

from skvs import *
import socket
import json

HOST = ''  # すべてのアドレスを受け付ける
PORT = 41224  # 待ち受けポート番号

kvs = SimpleKvs()

def get_operation_and_key(data):
    """
    クライアントから送られてくるjsonデータをデコードする
    """
    json_data = json.loads(data)
    return json_data["operation"], json_data["key"], json_data["value"]

# ソケットを作成し、IPアドレスとポート番号をバインド
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()  # 接続要求を待ち受ける

    print(f"Listening on port {PORT}...")
    
    while True:
        # 接続を受け付ける
        conn, addr = s.accept()
        print(f"Connected by {addr}")

        # クライアントからのデータを受信する
        data = conn.recv(1024)
        if not data:
            conn.close()
            break
        
        operation, key, value = get_operation_and_key(data)

        obj = {
            "result" : None,
            "operation" : operation
        }

        if operation == "get":
            result = kvs.get(key)
        elif operation == "put":
            result = kvs.put(key, value)
        elif operation == "delete":
            result = kvs.delete(key)
        elif operation == "scan":
            result = dict(kvs.scan())
            for k,v in result.items():
                result[k] = v.get_latest()

        obj["result"] = "" if result is None else result

        j_obj = json.dumps(obj)

        # クライアントに応答を送信する
        conn.sendall(j_obj.encode())

        # 接続を閉じる
        conn.close()
