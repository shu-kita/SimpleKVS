from flask import Flask, request
from simplekvs import SimpleKVS

app = Flask(__name__)
kvs = SimpleKVS("./data")
PORT = 30000

@app.route('/get')
def get():
    key = request.args.get('key')
    value = kvs.get(key)
    if value is None:
        return "Key not found"
    else:
        return value

@app.route('/set', methods=['POST'])
def set():
    key = request.args.get('key')
    value = request.args.get('value')
    kvs.set(key, value)
    return "OK"

@app.route('/delete', methods=['DELETE'])
def delete():
    key = request.args.get('key')
    kvs.delete(key)
    return "OK"

if __name__ == '__main__':
    app.run(port=PORT)