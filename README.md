# SimpleKVS

SimpleKVSは、LSM Tree を実装したKey-Value Storeです。  
※学習目的で作成

4/14～
　Javaの学習のため、Javaで実装中

## 使用方法

SimpleKVSクラスをインスタンス化して使う
```
from simplekvs import SimpleKVS

data_dir = "./data"
kvs = SimpleKVS(data_dir)

kvs.get("a")
kvs.set("b", "asdf")
kvs.delete("b")
```

### HTTP serverとして使う場合

<u>*※Flaskのインストールが必要*</u>

src配下で以下を実行する。
(別のディレクトリから実行する際は、相対パスを合わせる)
```
python ./http_server.py
```

ポート30000でアクセスを待ち受ける
また、実行ディレクトリ配下に「data」を作成し、そこにSSTable, index, walが保存される

http_server.pyの以下の箇所で、ポート、ディレクトリを指定できる
```
PORT = 30000
DATA_DIR = "./data" # SSTable, Index, walを保存するディレクトリ
```

curlなどのクライアントから実行する
<>内は可変
```
# get
curl -X GET http://<ホスト名>:30000/get/<key>

# set
curl -X POST http://<ホスト名>:30000/set/<key> -d <値>

# delete
curl -X DELETE http://<ホスト名>:30000/delete/<key>
```

## ファイル構成

memtableの要素数が1024を超えたら、SSTableにflashされる。
flash時にindexファイルも作成される。
```
data_dir
    ├─sstab_<unixtime>.dat # SSTable
    ├─sstab_<unixtime>.dat.index # indexファイル
    └─wal.dat # Write-Ahead Log
log_dir
    └─SimpleKVS.log # ApplicationのLogファイル
```

## TODO

* エラー処理がない

## ライセンス

SimpleKVSはMITライセンスの下でリリースされています。[LICENSEファイル](./LICENSE)を参照してください。