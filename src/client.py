import socket
import json

HOST = 'localhost'  # サーバーのホスト名またはIPアドレス
PORT = 41224        # サーバーの待ち受けポート番号

def send_request(operation, key, value):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        obj = {
            "operation" : operation,
            "key" : key,
            "value" : value
        }
        j_obj = json.dumps(obj)
        s.sendall(j_obj.encode())
    
        byte_data = s.recv(1024)
        data = byte_data.decode()
        print(f"Received: {data}")
        return data

def get(key):
    return send_request("get", key, "")

def put(key, value):
    return send_request("put", key, value)

def delete(key):
    return send_request("delete", key, "")

def scan():
    return send_request("scan", "", "")
