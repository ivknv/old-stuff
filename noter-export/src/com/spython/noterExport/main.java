package com.spython.noterExport;

import android.app.Activity;
import android.os.Bundle;
import android.content.Context;
import android.widget.Button;
import android.widget.EditText;
import android.view.View;
import android.view.View.OnClickListener;
import android.os.Environment;
import android.view.ContextMenu;
import android.view.ContextMenu.ContextMenuInfo;
import android.view.Gravity;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
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
		System.out.println(path);
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
					System.out.println(sdCardPath);
					File noter_directory = new File(sdCardPath + "/noter/" + username_value);
					if (!noter_directory.exists()) {
						noter_directory.mkdirs();
					}
					
					int exported_counter = 0;
					
					for (int i = 0; i < notes.size(); i++) {
						List note = (ArrayList) notes.get(i);
						String title = (String) note.get(1);
						String text = (String) note.get(3);
						String note_filename = title + ".html";
						note_filename = note_filename.replace(" ", "_");
						note_filename = note_filename.replaceAll("/|\\\\|\\?", "");
						text = "<!DOCTYPE html>\n<html>\t<head>\n\t\t<meta charset='utf-8' />\n\t\t<title>"+title+"</title>\n\t</head>\n\t<body>\n\t\t"+text+"\n\t</body>\n</html>";
						String dirname = sdCardPath + "/noter/"+ username_value;
						WriteFile file = new WriteFile(dirname, note_filename);
						try {
							file.writeToFile(text);
						} catch (IOException e) {
							Toast toast = Toast.makeText(getApplicationContext(), "Failed to save note", Toast.LENGTH_SHORT);
							toast.setGravity(Gravity.CENTER, 0, 0);
							toast.show();
							continue;
						}
						exported_counter++;
					}
					
					Toast toast = Toast.makeText(getApplicationContext(), "Exported "+exported_counter+" notes", Toast.LENGTH_SHORT);
					toast.setGravity(Gravity.CENTER, 0, 0);
					toast.show();
					break;
		}
	}
}
