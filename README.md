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

## ファイル構成

memtableの要素数が1024を超えたら、SSTableにflashされる
```
data_dir
    ├─sstab_<unixtime>.dat # データファイル
    ├─sstab_<unixtime>.dat.index # indexファイル
    └─wal.dat # Write-Ahead Log
```


## TODO

* String以外のオブジェクトが格納されることを想定していない
* delete()でSSTableのデータを消せない。
* Serverとして機能させたい(サーバ・クライアント)
* エラー処理がない
* ログの機能がない(以下の状況など)
  * 起動ログ
  * set, get, deleteの処理が走った時のログ
  * compaction実行時
  

## ライセンス

SimpleKVSはMITライセンスの下でリリースされています。[LICENSEファイル](./LICENSE)を参照してください。