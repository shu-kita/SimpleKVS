package com.shu.simplekvs;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.io.FileNotFoundException;
import java.nio.file.Files;

import java.util.Map;
import java.util.TreeMap;

public class SSTable {
    private Path path;
    private Map<String, Integer> index;

    // 以下のメソッドを実装する予定。
    // コンストラクタ(Flush時用(SSTableファイルに書き込む)と読み込み(Index読み込み用)の２種)
    // getメソッド
    // deleteメソッド(ファイルの消去メソッド)
    // (その他、Pythonの時必要だったメソッドを見ながら実装する方針)

    public SSTable(String path, TreeMap<String, String> memtable) {
        this.path = Paths.get(path);

        Long timestamp = System.currentTimeMillis();

        if (Files.isDirectory(this.path)) {
            Path file = Paths.get(String.format("sstab_%d.dat", timestamp));
            this.path = this.path.resolve(file);
        }

        //memtable書き込み処理
    }

    public SSTable(String path) throws FileNotFoundException{
        this.path = Paths.get(path);
        
        if (!Files.exists(this.path)) {
            throw new FileNotFoundException(String.format("%s is not found.", path));
        }

        // Index読み込み処理。
    }

    public static void main(String[] args) throws FileNotFoundException{
        // System.out.println("test");
        SSTable s = new SSTable("./adfsaf");
    }
}
