package com.shu.simplekvs;

import java.util.TreeMap;

public class Memtable extends TreeMap<String,String>{
    private int sizeLimit;
    
    public Memtable(int limit){
        this.sizeLimit = limit;
    }

    public Memtable() {
        this(1024);
    }

    private boolean is_overLimit() {
        return this.sizeLimit <= this.size();
    }

    public static void main(String[] args) {
        Memtable mt = new Memtable(100);
        boolean res = mt.is_overLimit();
        System.out.println(res);
    }
}
