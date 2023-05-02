package com.shu.simplekvs;

import java.io.BufferedOutputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
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

    public SSTable(String path, TreeMap<String, String> memtable) throws IOException{
        this.path = Paths.get(path);
        Long timestamp = System.currentTimeMillis();

        // TODO : 以下の修正
        //         pathのディレクトリがなかったら、pathの名前のファイルができてしまう
        if (Files.isDirectory(this.path)) {
            Path file = Paths.get(String.format("sstab_%d.dat", timestamp));
            this.path = this.path.resolve(file);
        }

        this.index = new HashMap<>();
        this.dumpKV(memtable);
        this.dumpIndex(this.index);
    }

    public SSTable(String path) throws FileNotFoundException{
        this.path = Paths.get(path);
        
        if (!Files.exists(this.path)) {
            throw new FileNotFoundException(String.format("%s is not found.", path));
        }

        // Index読み込み処理。
    }

    private void dumpKV(Map<String, String> memtable) throws IOException{
        try (
            FileOutputStream fos = new FileOutputStream(this.path.toString());
            BufferedOutputStream bos = new BufferedOutputStream(fos)
            ) {
        	    // indexにpositionをPutし、ファイルに書き込む
                int position = 0;
                for (Map.Entry<String, String> kv : memtable.entrySet()){
                    String key = kv.getKey();
                    String value = kv.getValue();
                    this.index.put(key, position);
                    position = key.length() + value.length() + 8;
                    IOUtils.dumpKV(bos, key, value);
                }
            }
    }
    
    private void dumpIndex(Map<String, Integer> index)  throws IOException{
    	String path = this.path.toString() + ".index";
    	try (
            FileOutputStream fos = new FileOutputStream(path);
    		BufferedOutputStream bos = new BufferedOutputStream(fos)
    	) {
    		for (Map.Entry<String, Integer> kp : this.index.entrySet()) {
    			String key = kp.getKey();
    			int position = kp.getValue();
    			IOUtils.dumpIndex(bos, key, position);
    		}
    	}
    }


    public static void main(String[] args) throws FileNotFoundException, IOException{
        // System.out.println("test");
        TreeMap<String, String> memtable = new TreeMap<String, String>();
        memtable.put("key1", "value1");
        memtable.put("key2", "value2");
        SSTable s = new SSTable("./test", memtable);
    }
}