package com.shu.simplekvs;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.ArrayList;
import java.util.TreeMap;
import java.util.Map;

class SimpleKVS {
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

    public static void main(String[] args) {
        //test用

        SimpleKVS skvs = new SimpleKVS(".", 1024);
        System.out.println(skvs.memtable);
        System.out.println(skvs.dataDir);
        System.out.println(skvs.memtableLimit);
        System.out.println(skvs.sstableList);
        //skvs.memtable;
    }
}