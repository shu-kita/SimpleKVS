package com.shu.simplekvs;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;

import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;

public class KVSRequestHandler implements HttpHandler{
	
	public void handle(HttpExchange t) throws IOException{
		String startLine = this.getStartLine(t);
		System.out.println(startLine);

		Headers reqHeaders = t.getRequestHeaders();
		for (String name : reqHeaders.keySet()) {
			System.out.println(name + ": " + reqHeaders.getFirst(name));
	    }
		
		InputStream is = t.getRequestBody();
		byte[] b = is.readAllBytes();
		is.close();
		if (b.length != 0) {
			System.out.println(); // 空行
			System.out.println(new String(b, StandardCharsets.UTF_8));
		}
		
		String resBody = this.createResBody(t);
		Headers resHeaders = this.createResHeader(t);
		
		// レスポンスヘッダを送信
		int statusCode = 200;
		long contentLength = resBody.getBytes(StandardCharsets.UTF_8).length;
		t.sendResponseHeaders(statusCode, contentLength);

		// レスポンスボディを送信
		OutputStream os = t.getResponseBody();
		os.write(resBody.getBytes());
		os.close();
	}
	
	private String getStartLine(HttpExchange t) {
		String startLine = t.getRequestMethod() + " " +
			      		   t.getRequestURI().toString() + " " +
			      		   t.getProtocol();
		return startLine;
	}

	private String createResBody(HttpExchange t) {
		String resBody = switch (t.getRequestURI().toString()) {
			case "/hello" -> "{\"message\": \"Hello, World!\"}";
			case "/get" -> "{\"value\": \"-VALUE-\"}";
			case "/put" -> "{\"result\": \" OK \"}";
			case "/delete" -> "{\"resutl\": \" OK \"}";
	        default -> "{\"message\": \"Invalid URL\"}";
	      };
	      return resBody;
	}
	
	private Headers createResHeader(HttpExchange t) {
		Headers resHeaders = t.getResponseHeaders();
		resHeaders.set("Content-Type", "application/json");
		resHeaders.set("Last-Modified",
				ZonedDateTime.now(ZoneOffset.UTC).format(DateTimeFormatter.RFC_1123_DATE_TIME));
		resHeaders.set("Server",
				"MyServer (" +
				System.getProperty("java.vm.name") + " " +
				System.getProperty("java.vm.vendor") + " " +
				System.getProperty("java.vm.version") + ")"
				);
		return resHeaders;
	}
	
}

