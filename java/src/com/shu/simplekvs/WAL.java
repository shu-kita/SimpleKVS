package com.shu.simplekvs;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Map;
import java.util.TreeMap;

public class WAL {
    private Path path;

    public WAL(String dataDir) {
        this.path = Paths.get(dataDir);
        Path file = Paths.get(String.format("wal.dat"));
        this.path = this.path.resolve(file);        
    }

    public WAL() {
        this(".");
    }

    protected void set(String key, String value) throws IOException{
    	try (
            FileOutputStream fos = new FileOutputStream(this.path.toString(),true);
            BufferedOutputStream bos = new BufferedOutputStream(fos)
        ) {
    		IOUtils.dumpKV(bos, key, value);
    	}
    }

    protected Map<String, String> recovery() throws IOException{
    	Map<String, String> memtable = new TreeMap<String, String>();
    	try(
        	FileInputStream fis = new FileInputStream(this.path.toString());
        	BufferedInputStream bis = new BufferedInputStream(fis)
        ) {
    		while (bis.available() > 1) {
    			String[] kv = IOUtils.loadKV(bis, 0);
    			String key = kv[0];
    			String value = kv[1];
    			memtable.put(key, value);
    		}
    		return memtable;
    	}
    }

    protected void cleanUp() throws IOException{
    	FileOutputStream fos = new FileOutputStream(this.path.toString(), false);
    	fos.close();
    }
}