package com.shu.simplekvs;

import java.nio.file.Path;
import java.util.Map;

public class SSTable {
    private Path path;
    private Map<String, Integer> index;

    // 以下のメソッドを実装する予定。
    // コンストラクタ(Flush時用(SSTableファイルに書き込む)と読み込み(Index読み込み用)の２種)
    // getメソッド
    // deleteメソッド(ファイルの消去メソッド)
    // (その他、Pythonの時必要だったメソッドを見ながら実装する方針)
}
