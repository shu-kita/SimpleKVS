package com.shu.simplekvs;

import java.nio.file.Path;
import java.nio.file.Paths;

public class WAL {
    Path path;

    public WAL(String path) {
        this.path = Paths.get(path);
    }

    public WAL() {
        this(".");
    }

    protected void set(String key, String value) {
        // WALへの書き込み処理
    }

    protected void recovery() {
        // WALからMemtableを復元する処理
        // TreeMapを返すべき？？？
    }

    protected void cleanUp() {
        // WALを空にする
    }

    public static void main(String args []) {
        WAL wal = new WAL();
        System.out.println(wal);
    }
}
