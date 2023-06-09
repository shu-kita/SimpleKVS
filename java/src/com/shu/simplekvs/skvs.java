package com.shu.simplekvs;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class skvs {
	private static final String help = """
			get, deleteの時
			    java skvs <get or delete> <key>
			putの時
			    java skvs put <key> <value>
			""";
	
	public static void main(String[] args) {
		if (!skvs.checkArgs(args)) {
			System.out.println(String.format("""
					[ERROR] 引数が間違っています
					Usage :					
					%s
					""", skvs.help));
			return;
		}
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
	
	private static boolean checkArgs(String args[]) {
		if (args.length == 0) {
			return false;
		}
		
		boolean result = switch (args[0]) {
		case "get", "delete"-> args.length == 2 ? true : false;
		case "put"-> args.length == 3 ? true : false;
		default -> false;
		};
		return result;
	}
}
