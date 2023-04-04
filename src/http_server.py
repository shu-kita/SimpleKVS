from flask import Flask, request
from simplekvs import SimpleKVS

PORT = 30000
DATA_DIR = "./data" # SSTable, Index, walを保存するディレクトリ

app = Flask(__name__)
kvs = SimpleKVS(DATA_DIR)

@app.route('/get/<key>')
def get(key):
    value = kvs.get(key)
    if value is not None:
        return value
    else:
        return "Key not found"

@app.route('/set/<key>', methods=['POST'])
def set(key):
    value = request.get_data()
    value = value.decode("utf-8")
    kvs.set(key, value)
    return "OK"

@app.route('/delete/<key>', methods=['DELETE'])
def delete(key):
    if key in kvs:
        kvs.delete(key)
        return "OK"
    else:
        return "Key not found"

if __name__ == '__main__':
    app.run(port=PORT)