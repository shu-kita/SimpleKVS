import logging
import socket
from pathlib import Path
from flask import Flask, request
from simplekvs import SimpleKVS

PORT = 30000
DATA_DIR = "./data" # SSTable, Index, walを保存するディレクトリ
LOG_FILE = Path("./log/SimpleKVS.log")

if not LOG_FILE.parent.exists():
    LOG_FILE.parent.mkdir(parents=True)

logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO,
    encoding="utf-8"
    )

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

    logging.info("Starting HTTP Server...")
    hostname = socket.gethostname()
    logging.info(f"Running on http://{hostname}:{PORT}")

    app.run(port=PORT)
    # ログファイル、フォーマット指定

