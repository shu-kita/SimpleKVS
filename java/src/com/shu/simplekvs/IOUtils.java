package com.shu.simplekvs;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.ByteBuffer;

public class IOUtils {
    // KeyとValueをファイルに書き込む関数
    public static void dumpKV(String key, String value) throws IOException {
        // keyをbyte配列にエンコードし、長さを取得
        byte[] byteKey = key.getBytes(StandardCharsets.UTF_8);
        int keyLength = byteKey.length;
        byte[] keyLenBytes = ByteBuffer.allocate(4).putInt(keyLength).array();

        // valueをbyte配列にエンコードし、長さを取得
        byte[] byteValue = value.getBytes(StandardCharsets.UTF_8);
        int valueLength = byteValue.length;
        byte[] valueLenBytes = ByteBuffer.allocate(4).putInt(valueLength).array();
        
        // byte配列の結合
        byte[] writeBytes = IOUtils.combineBytes(keyLenBytes, byteKey, valueLenBytes, byteValue);

        String testfile = "test.dat"; // ファイル名(引数で引き取る)
        // TODO : 追記ができるようにする
        try (
            FileOutputStream fos = new FileOutputStream(testfile);
            BufferedOutputStream bos = new BufferedOutputStream(fos)){
                bos.write(writeBytes);
                bos.write(writeBytes);
        }
    }

    public static String[] loadKV(int position) throws IOException {
        String testfile = "test.dat"; // ファイル名(引数で引き取る)
        try (
            FileInputStream fis = new FileInputStream(testfile);
            BufferedInputStream bis = new BufferedInputStream(fis)){
                String[] kvPair = new String[2]; 
                bis.skip(position);
                for (int i = 0 ; i < 2; i++) {
                    byte[] bytes = new byte[4];
                    bis.read(bytes, 0, bytes.length);
                    int length = ByteBuffer.wrap(bytes).getInt();
                    byte[] byteKey = new byte[length];
                    bis.read(byteKey, 0, byteKey.length);
                    kvPair[i] = new String(byteKey);
                }
                // indexの0をキー、1をバリューとするString配列を返す
                return kvPair;
            }
    }

    // 4つのByte配列を結合する関数
    protected static byte[] combineBytes(byte[] byteArray1, byte[] byteArray2, byte[] byteArray3, byte[] byteArray4) {
        // 各配列の長さを取得
        int length1 = byteArray1.length;
        int length2 = byteArray2.length;
        int length3 = byteArray3.length;
        int length4 = byteArray4.length;

        byte[] combinedArray = new byte[length1 + length2 + length3 + length4];

        // 順に結合
        System.arraycopy(byteArray1, 0, combinedArray, 0, length1);
        System.arraycopy(byteArray2, 0, combinedArray, length1, length2);
        System.arraycopy(byteArray3, 0, combinedArray, (length1+length2), length3);
        System.arraycopy(byteArray4, 0, combinedArray, (length1+length2+length3), length4);

        return combinedArray;
    }

    public static void main(String[] args) throws IOException{
        String[] kv = IOUtils.loadKV(0);
        for (String item: kv){
            System.out.println(item);
        }
    }
}
