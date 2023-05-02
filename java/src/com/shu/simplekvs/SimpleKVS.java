package com.shu.simplekvs;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public class SimpleKVS {
    private Path dataDir;
    private Map<String, String> memtable;
    private int memtableLimit;
    private List<SSTable> sstableList;

    public SimpleKVS(String dataDir, int memtableLimit) {
        this.dataDir = Paths.get(dataDir);
        this.memtable = new TreeMap<String, String>();
        this.memtableLimit = memtableLimit;
        this.sstableList = new ArrayList<SSTable>(); 
    }

    public SimpleKVS(String dataDir) {
        this(dataDir, 1024);
    }

    public SimpleKVS() {
        this(".", 1024);
    }

    public String get(String key) {
    	// TODO : valueをどこでreturnするか決めないといけない
    	String value = null;
        if (this.memtable.containsKey(key)) {
            value = this.memtable.get(key);
            if (this.isDeleted(value)) {
                value = null;
            }
            return value;
        } else {
        	try {
        		for (SSTable sstable : this.sstableList) {
                	value = sstable.get(key);
                	if (value != null) {
                		return value;
                	}
            	}
        	} catch (IOException e) {
        		e.printStackTrace();
        	}
        	return value;
        }
    }

    public void set(String key, String Value) {
        // walへの書き込み処理
        this.memtable.put(key, Value);
        if (this.memtable.size() >= this.memtableLimit) {
        	try {
        		SSTable sstable = new SSTable(this.dataDir.toString() , this.memtable);
        		this.sstableList.add(sstable);
                this.memtable = new TreeMap<String, String>();
        	} catch (IOException e){
        		e.printStackTrace();
        	}
        	
        }
    }

    public void delete(String key) {
        // walへの書き込み処理
        this.memtable.put(key, "__tombstone__");
    }

    protected boolean isDeleted(String value) {
        if (value.equals("__tombstone__")) {
            return true;
        } else {
            return false;
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