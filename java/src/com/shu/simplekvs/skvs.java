package com.shu.simplekvs;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class skvs {
	public static void main(String[] args) {
		// クライアントソケットを生成
		try (Socket socket = new Socket("localhost", 10000);
			 PrintWriter writer = new PrintWriter(socket.getOutputStream(), true);
			 BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()))
		) {
			String message = String.join(" ", args);
			writer.println(message);
			System.out.println(reader.readLine());
		} catch (IOException e){
			e.printStackTrace();
		}
	}
}
