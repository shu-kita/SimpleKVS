package com.shu.simplekvs;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.ArrayList;
import java.util.TreeMap;
import java.util.Map;

public class SimpleKVS {
    private Path dataDir;
    private Map<String, String> memtable;
    private int memtableLimit;
    private List<String> sstableList;

    public SimpleKVS(String dataDir, int memtableLimit) {
        this.dataDir = Paths.get(dataDir);
        this.memtable = new TreeMap<String, String>();
        this.memtableLimit = memtableLimit;
        this.sstableList = new ArrayList<String>(); 
    }

    public SimpleKVS(String dataDir) {
        this(dataDir, 1024);
    }

    public SimpleKVS() {
        this(".", 1024);
    }

    public String get(String key) {
        if (this.memtable.containsKey(key)) {
            String value = this.memtable.get(key);
            if (this.isTombstone(value)) {
                value = null; 
            }
            return value;
        } else {
            // SSTableから読み込む処理
            return "not found!";
        }
    }

    public void set(String key, String Value) {
        // walへの書き込み処理
        this.memtable.put(key, Value);
        if (this.memtable.size() >= this.memtableLimit) {
            // SSTableにFlushする処理 
        }
    }

    public void delete(String key) {
        // walへの書き込み処理
        this.memtable.put(key, "__tombstone__");
    }

    protected boolean isTombstone(String value) {
        if (value.equals("__tombstone__")) {
            return false;
        } else {
            return true;
        }
    }

    public static void main(String[] args) {
        //test用

        SimpleKVS skvs = new SimpleKVS(".", 1024);
        System.out.println(skvs.memtable);
        System.out.println(skvs.dataDir);
        System.out.println(skvs.memtableLimit);
        System.out.println(skvs.sstableList);
        skvs.set("1", "mura");
        for (int i=0 ;  i < 1050; i++){
            String num = Integer.valueOf(i).toString();
            skvs.set(num, "kita");
        }
        System.out.println(skvs.get("19192939"));
        //skvs.memtable;
    }
}