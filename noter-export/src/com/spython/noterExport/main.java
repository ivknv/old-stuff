package com.spython.noterExport;

import android.app.Activity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.view.View;
import android.view.View.OnClickListener;
import android.os.Environment;
import android.view.Gravity;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.IOException;
import java.io.File;
import java.io.OutputStreamWriter;
import java.io.FileOutputStream;

import java.util.List;
import java.util.ArrayList;

import org.json.simple.JSONObject;
import org.json.simple.JSONArray;
import org.json.simple.parser.JSONParser;

class WriteFile {
	private String path;
	private String filename;
	
	public WriteFile(String directory, String fname) {
		path = directory;
		filename = fname;
	}
	
	public void writeToFile(String textLine) throws IOException {
		File file = new File(path, filename);
		
		if (!file.exists()) {
			try {
				file.createNewFile();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		FileOutputStream write = new FileOutputStream(file);
		OutputStreamWriter osw = new OutputStreamWriter(write);
		
		osw.write(textLine);
		
		osw.close();
	}
}

class Noter {
	private static final String USER_AGENT = "Mozilla/5.0";
	
	private static String sendPostRequest(String url, String parameters) throws Exception {
		url = "http://web-noter.herokuapp.com/api/" + url + "/";
		URL obj = new URL(url);
		HttpURLConnection con = (HttpURLConnection) obj.openConnection();
		con.setRequestMethod("POST");
		con.setRequestProperty("User-Agent", USER_AGENT);
		
		con.setDoOutput(true);
		
		DataOutputStream wr = new DataOutputStream(con.getOutputStream());
		wr.writeBytes(parameters);
		wr.flush();
		wr.close();
		
		BufferedReader in = new BufferedReader(
			new InputStreamReader(con.getInputStream())
		);
		
		String inputLine;
		StringBuffer response = new StringBuffer();
		
		while ((inputLine = in.readLine()) != null) {
			response.append(inputLine);
		}
		
		in.close();
		String jsonString = response.toString();
		
		return jsonString;
	}
	
	public static List getNotes(String username, String password) {
		JSONParser parser = new JSONParser();
		JSONArray notes;
		try {
			notes = (JSONArray) parser.parse(
				sendPostRequest("getNotes",
					"username=" +
					username +
					"&password=" +
					password)
			);
		} catch (Exception e) {
			e.printStackTrace();
			return (List) new ArrayList();
		}
		
		List notes_list = new ArrayList();
		
		for (int i = 0; i < notes.size(); i++) {
			JSONObject note = (JSONObject) notes.get(i);
			JSONObject fields = (JSONObject) note.get("fields");
			List note_list = new ArrayList();
			note_list.add(note.get("pk"));
			note_list.add(fields.get("title"));
			note_list.add(fields.get("date"));
			note_list.add(fields.get("text"));
			note_list.add(fields.get("tags"));
			note_list.add(fields.get("type"));
			
			notes_list.add(note_list);
		}
		
		return notes_list;
	}
}


public class main extends Activity implements OnClickListener {
	
	private Button btn;
	private EditText username;
	private EditText password;
	
	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main);
		
		btn = (Button) findViewById(R.id.export);
		username = (EditText) findViewById(R.id.username);
		password = (EditText) findViewById(R.id.password);
		btn.setOnClickListener(this);
	}
	
	@Override
	public void onClick(View v) {
		switch (v.getId()) {
			case R.id.export:
					String username_value = username.getText().toString();
					String password_value = password.getText().toString();
					
					List notes = (ArrayList) Noter.getNotes(username_value, password_value);
					
					String sdCardPath = Environment.getExternalStorageDirectory().getAbsolutePath();
					File noter_directory = new File(sdCardPath + "/noter/" + username_value);
					if (!noter_directory.exists()) {
						noter_directory.mkdirs();
					}
					
					String noter_directory_path = noter_directory.getAbsolutePath();
					
					int exported_counter = 0;
					int fail_counter = 0;
					
					for (int i = 0; i < notes.size(); i++) {
						List note = (ArrayList) notes.get(i);
						long note_id = (Long) note.get(0);
						String title = (String) note.get(1);
						String title1 = title.replaceAll("&", "&amp;");
						title1 = title1.replaceAll("<", "&lt;");
						title1 = title1.replaceAll(">", "&gt;");
						String text = (String) note.get(3);
						
						text = text.replaceAll("\\n", "<br/>");
						String note_filename = title + ".html";
						note_filename = note_filename.replaceAll(" ", "_");
						note_filename = note_filename.replaceAll("/", "-slash-");
						note_filename = note_filename.replaceAll("\\\\", "-backslash-");
						note_filename = note_filename.replaceAll("\\?", "-question mark-");
						note_filename = note_filename.replaceAll("<", "-lt-");
						note_filename = note_filename.replaceAll(">", "-gt-");
						text = "<!DOCTYPE html>\n"+
						"<html>\n"+
						"	<head>\n"+
						"<meta name='viewport' content='width=device-width, initial-scale=1.0' />\n"+
						"		<meta charset='utf-8' />\n"+
						"		<title>"+title+"</title>\n"+
						"		<style type='text/css'>\n"+
						"			html, body, div, span,\n"+
						"			h1, h2, h3, h4, h5, h6, p, pre,\n"+
						"			a, code, img, kbd, samp,\n"+
						"			small, var,\n"+
						"			form, label,\n"+
						"			article, aside, canvas,\n"+
						"			footer, header, hgroup,\n"+
						"			nav, section,\n"+
						"			time {\n"+
						"				margin: 0;\n"+
						"				padding: 0;\n"+
						"				border: 0;\n"+
						"				font-size: 100%;\n"+
						"				font: inherit;\n"+
						"				vertical-align: baseline;\n"+
						"			}\n"+
						"			mark {\n"+
						"				padding: 0;\n"+
						"				border: none;\n"+
						"				font-family: inherit;\n"+
						"				vertical-align: baseline;\n"+
						"				font-size: 100%;\n"+
						"				background-color: rgb(255, 255, 0);\n"+
						"				box-shadow: inset 0 0 20px rgb(255, 255, 255);\n"+
						"			}\n"+
						"			article, aside, details, figcaption, figure,\n"+
						"			footer, header, hgroup, menu, nav, section {\n"+
						"				display: block;\n"+
						"			}\n"+
						"			code {\n"+
						"					display: inline-block;\n"+
						"					background-color: rgb(249, 242, 244);\n"+
						"					color: rgb(199, 37, 78);\n"+
						"					padding: 2px 4px;\n"+
						"					line-height: 1.42857;\n"+
						"					border-radius: 4px;\n"+
						"					font-size: 90%;\n"+
						"					margin-top: 1px;\n"+
						"					margin-bottom: 1px;\n"+
						"			}\n"+
						"			kbd {\n"+
						"				background-color:#333;\n"+
						"				border-radius:4px;\n"+
						"				color: #FFF;\n"+
						"				display:inline-block;\n"+
						"				line-height:1.42587;\n"+
						"				margin-bottom:1px;\n"+
						"				margin-top:1px;\n"+
						"				padding:2px 4px;\n"+
						"			}\n"+
						"			img {\n"+
						"				max-width: 100%;\n"+
						"				max-height: 100%;\n"+
						"			}\n"+
						"			h1, h2, h3, h4, h5, h6 {\n"+
						"		   		font-weight: bold;\n"+
						"				color: rgb(67, 74, 84);\n"+
						"			}\n"+
						"			h2 {\n"+
						"				font-size: 38px;\n"+
						"			}\n"+
						"			h1 {\n"+
						"				font-size: 50px;\n"+
						"			}\n"+
						"			h3 {\n"+
						"				font-size: 20px;\n"+
						"			}\n"+
						"			h4 {\n"+
						"				font-size: 18px;\n"+
						"			}\n"+
						"			h5 {\n"+
						"				font-size: 16px;\n"+
						"			}\n"+
						"			h6 {\n"+
						"				font-size: 14px;\n"+
						"			}\n"+
						"			p {\n"+
						"				margin-top: 5px;\n"+
						"				margin-bottom: 5px;\n"+
						"			}\n"+
						"			a {\n"+
						"				text-decoration: none;\n"+
						"				color: rgb(0, 155, 255);\n"+
						"				outline: 0;\n"+
						"			}\n"+
						"			a:hover {\n"+
						"				color:rgb(0, 191, 255);\n"+
						"			}\n"+
						"			pre {\n"+
						"				padding:0;\n"+
						"				font-size:14px;\n"+
						"				font-family:Monospace, Courier, Sans-serif;\n"+
						"				line-height:1.1;\n"+
						"				word-wrap:break-word;\n"+
						"				white-space:pre-wrap;\n"+
						"				white-space:-moz-pre-wrap;\n"+
						"				white-space:-o-pre-wrap;\n"+
						"				white-space:-pre-wrap;\n"+
						"			}\n"+
						"			article {\n"+
						"				word-wrap:break-word;\n"+
						"				max-width:1000px;\n"+
						"				min-wdth:240px;\n"+
						"				padding:0px 5px;\n"+
						"			}\n"+
						"			article p {\n"+
						"				font-size:18px;\n"+
						"			}\n"+
						"			article .title {\n"+
						"				margin-bottom: 5px;\n"+
						"				min-width: 240px;\n"+
						"				text-decoration: none;\n"+
						"				font-size: 24px;\n"+
						"				font-family: Helvetica, Verdana, Arial;\n"+
						"				color: rgb(86, 174, 61);\n"+
						"				opacity: 0.9;\n"+
						"				transition: opacity 1s ease-in-out, color 0.5s ease-in;\n"+
						"				-moz-transition: opacity 1s ease-in-out, color 0.5s ease-in;\n"+
						"				-webkit-transition: opacity 1s ease-in-out, color 0.5s ease-in;\n"+
						"				-o-transition: opacity 1s ease-in-out, color 0.5s ease-in;\n"+
						"				-ms-transition: opacity 1s ease-in-out, color 0.5s ease-in;\n"+
						"			}\n"+
						"			article .title:hover {\n"+
						"				opacity:1;\n"+
						"				color:rgb(106, 194, 81);\n"+
						"			}\n"+
						"		</style>\n"+
						"	</head>\n"+
						"	<body>\n"+
						"		<article>\n"+
						"			<a href='http://web-noter.herokuapp.com/note/"+note_id+"'>\n"+
						"				<span class='title'>"+title1+"</span>\n"+
						"			</a>\n"+
						"			<p>"+text+"</p>\n"+
						"	</body>\n"+
						"</html>";
						WriteFile file = new WriteFile(noter_directory_path, note_filename);
						try {
							file.writeToFile(text);
						} catch (IOException e) {
							fail_counter++;
							continue;
						}
						exported_counter++;
					}
					
					Toast success_toast = Toast.makeText(getApplicationContext(), "Exported "+exported_counter+" notes to " + noter_directory_path, Toast.LENGTH_SHORT);
					success_toast.setGravity(Gravity.CENTER, 0, 0);
					success_toast.show();
					Toast fail_toast = Toast.makeText(getApplicationContext(), "Failed to save "+fail_counter+" notes", Toast.LENGTH_SHORT);
					fail_toast.setGravity(Gravity.CENTER, 0, 0);
					fail_toast.show();
					break;
		}
	}
}
