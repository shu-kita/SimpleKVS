package com.shu.simplekvs;

import java.io.File;
import java.io.IOException;
import java.nio.channels.OverlappingFileLockException;
import java.nio.file.Files;
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
    private WAL wal;

    public SimpleKVS(String dataDir, int memtableLimit) {
        this.dataDir = Paths.get(dataDir);
        
        // ディレクトリが存在しない場合、作成する
        if (!Files.exists(this.dataDir)) {
        	try {
        		Files.createDirectories(this.dataDir);
        	} catch (IOException e) {
        		e.printStackTrace();
        	}
        }
        
        this.memtable = new TreeMap<String, String>();
        this.memtableLimit = memtableLimit;
        this.sstableList = new ArrayList<SSTable>();
        
        // SSTable読み込み処理
        File[] files = new File(dataDir).listFiles();
        for (File file : files) {
        	String path = file.getPath();
        	if (path.startsWith("sstab") && path.endsWith(".dat")) {
        		try {
        			this.sstableList.add(new SSTable(path));
        		} catch (IOException e) {
        			// TODO : SSTableが読み込めなかった時の処理
        			e.printStackTrace();
        		}
        	}
        }
        
        this.wal = new WAL(dataDir);
        
        try {
        	this.wal.recovery();
        } catch (IOException e) {
        	// TODO
        	//   * 強制終了させる処理
        	//   * log出力処理
        	e.printStackTrace();
        }
    }

    public SimpleKVS(String dataDir) {
        this(dataDir, 1024);
    }

    public SimpleKVS() {
        this(".", 1024);
    }

    public String get(String key) {
    	String value = "";
    	if (this.memtable.containsKey(key)) {
    		// memtableから取得する
            value = this.memtable.get(key);
            value = this.isDeleted(value) ? null : value;
        } else {
        	// SSTableから取得する
        	try {
        		for (SSTable sstable : this.sstableList) {
                	if (sstable.containsKey(key)) {
                		value = sstable.get(key);
                		break;
                	}
            	}
        	} catch (IOException e) {
        		e.printStackTrace();
        	}
        }
    	// 削除されているかチェックしてreturn
    	return this.isDeleted(value) ? null : value;
    }

    public void set(String key, String value) {
    	this.writeWAL(key, value);
        this.memtable.put(key, value);
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
        this.writeWAL(key, "__tombstone__");
        this.memtable.put(key, "__tombstone__");
    }


    /*
     以下、privateのメソッド
     */ 
    private boolean isDeleted(String value) {
        return value.equals("__tombstone__");
    }
    
    private void writeWAL(String key, String value) {
    	try {
    		this.wal.set(key, value);
    	} catch (OverlappingFileLockException e) {
    		// TODO : Lockできなかった時の処理(ログ出力？？）
    		e.printStackTrace();
    	} catch (IOException e) {
    		e.printStackTrace();
    	}
    }
}