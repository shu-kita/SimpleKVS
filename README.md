# SimpleKVS

SimpleKVSは、簡単にKeyとValueのセット保存するためのPythonモジュールです。

## 使用方法

* Server
    ```
    python server.py
    ```
    ポート41224で待機する。


* Client
```
import client

# get
client.get("1")

# put
client.put("1", "test")

# delete
client.delete("1")

# scan
client.scan()
```

## ライセンス

SimpleKVSはMITライセンスの下でリリースされています。[LICENSEファイル](./LICENSE)を参照してください。