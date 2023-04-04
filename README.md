# SimpleKVS

SimpleKVSは、LSM Tree を実装したKey-Value Storeです。  
※学習目的で作成

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
```
# get
curl -X GET http://<ホスト名>:30000/get?key=<キー>

# set
curl -X POST "http://<ホスト名>:30000/set?key=<キー>&value=<値>"

# delete
curl -X DELETE http://<ホスト名>:30000/delete?key=<キー>
```

## ファイル構成

memtableの要素数が1024を超えたら、SSTableにflashされる。
flash時にindexファイルも作成される。
```
data_dir
    ├─sstab_<unixtime>.dat # SSTable
    ├─sstab_<unixtime>.dat.index # indexファイル
    └─wal.dat # Write-Ahead Log
```

## TODO

* String以外のオブジェクトが格納されることを想定していない
  * byte化できるものならなんでも格納できるを目標にしたい
* Compactionを定期的に実行する
  * minor, majorがあり、どちらをどんな条件で実行するかを決めないといけない
* エラー処理がない
* ログの機能がない(以下の状況など)
  * 起動ログ
  * set, get, deleteの処理が走った時のログ
  * compaction実行時
  

## ライセンス

SimpleKVSはMITライセンスの下でリリースされています。[LICENSEファイル](./LICENSE)を参照してください。