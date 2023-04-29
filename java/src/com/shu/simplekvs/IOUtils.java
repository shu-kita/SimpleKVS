package com.shu.simplekvs;

import java.io.FileInputStream;
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.ByteBuffer;
import java.util.HashMap;
import java.util.Map;

public class IOUtils {
    // KeyとValueをファイルに書き込む関数
    public static void dumpKV(BufferedOutputStream bos, String key, String value) throws IOException {
        // TODO : 書き込んだ位置を返すようにする必要がある？？
        //        (もしくは、SSTable側で位置を管理する)

        // keyをbyte配列にエンコードし、長さを取得
        byte[][] KeyAndLen = IOUtils.getBytekeyAndLength(key);
        byte[] byteKey = KeyAndLen[0];
        byte[] keyLenBytes = KeyAndLen[1];

        // valueをbyte配列にエンコードし、長さを取得
        byte[] byteValue = value.getBytes(StandardCharsets.UTF_8);
        int valueLength = byteValue.length;
        byte[] valueLenBytes = ByteBuffer.allocate(4).putInt(valueLength).array();
        
        // byte配列の結合
        byte[] writeBytes = IOUtils.combineBytes(keyLenBytes, byteKey, valueLenBytes, byteValue);

        // TODO : 追記ができるようにする
        bos.write(writeBytes);
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
                    byte[] byteStr = new byte[length];
                    bis.read(byteStr, 0, byteStr.length);
                    kvPair[i] = new String(byteStr);
                }
                // indexの0をキー、1をバリューとするString配列を返す
                return kvPair;
            }
    }

    public static void dumpIndex(BufferedOutputStream bos, String key, int position) throws IOException {
        byte[][] KeyAndLen = IOUtils.getBytekeyAndLength(key);
        byte[] byteKey = KeyAndLen[0];
        byte[] keyLenBytes = KeyAndLen[1];

        byte[] posBytes = ByteBuffer.allocate(4).putInt(position).array();

        byte[] writeBytes = IOUtils.combineBytes(keyLenBytes, byteKey, posBytes);
        // TODO : 追記ができるようにする
        bos.write(writeBytes);
    }

    public static  Map<String, Integer> loadIndex() throws IOException {
        String testfile = "test.dat.index";// ファイル名(引数で引き取るようにしたい)
        Map<String, Integer> index = new HashMap<>();
        try (
            FileInputStream fis = new FileInputStream(testfile);
            BufferedInputStream bis = new BufferedInputStream(fis)){
                byte[] bytes = new byte[4];
                int read;
                while ((read = bis.read(bytes, 0, bytes.length)) != -1) {
                    int length = ByteBuffer.wrap(bytes).getInt();
                    byte[] byteKey = new byte[length];
                    bis.read(byteKey, 0, byteKey.length);

                    bis.read(bytes, 0, bytes.length);
                    String key = new String(byteKey);
                    int position = ByteBuffer.wrap(bytes).getInt();
                    index.put(key, position);
                }
            }
        return index;
    }

    protected static byte[][] getBytekeyAndLength(String key) {
        byte[][] bytes = new byte[2][];
        bytes[0] = key.getBytes(StandardCharsets.UTF_8);
        int keyLength = bytes[0].length;
        bytes[1] = ByteBuffer.allocate(4).putInt(keyLength).array();
        return bytes;
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

    // 3つのByte配列を結合する関数
    protected static byte[] combineBytes(byte[] byteArray1, byte[] byteArray2, byte[] byteArray3) {
        // 各配列の長さを取得
        int length1 = byteArray1.length;
        int length2 = byteArray2.length;
        int length3 = byteArray3.length;

        byte[] combinedArray = new byte[length1 + length2 + length3];

        // 順に結合
        System.arraycopy(byteArray1, 0, combinedArray, 0, length1);
        System.arraycopy(byteArray2, 0, combinedArray, length1, length2);
        System.arraycopy(byteArray3, 0, combinedArray, (length1+length2), length3);

        return combinedArray;
    }
}
