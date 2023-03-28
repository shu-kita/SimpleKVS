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

def result_parse(result):
    j_obj = json.loads(result)
    return j_obj["result"]

def get(key):
    res = send_request("get", key, "")
    return result_parse(res)

def put(key, value):
    res = send_request("put", key, value)
    return result_parse(res)

def delete(key):
    res = send_request("delete", key, "")
    return result_parse(res)

def scan():
    res =  send_request("scan", "", "")
    return result_parse(res)
