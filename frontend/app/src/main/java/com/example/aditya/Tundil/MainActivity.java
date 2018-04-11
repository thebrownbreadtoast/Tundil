package com.example.aditya.Tundil;

import android.app.Activity;
import android.content.Intent;
import android.database.DataSetObserver;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.Gravity;
import android.view.KeyEvent;
import android.view.View;
import android.widget.AbsListView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;


public class MainActivity extends Activity {
    private static final String TAG = "ChatActivity";

    private ChatArrayAdapter chatArrayAdapter;
    private ListView listView;
    private EditText chatText;
    private Button buttonSend;
    private Convert con = new Convert();

    private String message="";
    private String reply="";

    private String apikey;
    private String ip;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);

        Bundle bundle = getIntent().getExtras();

        apikey = bundle.getString("ApiKey");
        ip = bundle.getString("IP");

        buttonSend = (Button) findViewById(R.id.send);

        listView = (ListView) findViewById(R.id.msgview);

        chatArrayAdapter = new ChatArrayAdapter(getApplicationContext(), R.layout.right);
        listView.setAdapter(chatArrayAdapter);

        chatText = (EditText) findViewById(R.id.msg);
        chatText.setOnKeyListener(new View.OnKeyListener() {
            public boolean onKey(View v, int keyCode, KeyEvent event) {
                if ((event.getAction() == KeyEvent.ACTION_DOWN) && (keyCode == KeyEvent.KEYCODE_ENTER)) {
                    return sendChatMessage();
                }
                return false;
            }
        });
        buttonSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View arg0) {
                sendChatMessage();
            }
        });

        listView.setTranscriptMode(AbsListView.TRANSCRIPT_MODE_ALWAYS_SCROLL);
        listView.setAdapter(chatArrayAdapter);

        //to scroll the list view to bottom on data change
        chatArrayAdapter.registerDataSetObserver(new DataSetObserver() {
            @Override
            public void onChanged() {
                super.onChanged();
                listView.setSelection(chatArrayAdapter.getCount() - 1);
            }
        });
    }

    private boolean sendChatMessage()   {
        if(chatText.getText().toString().length() == 0)
        {
            Toast t = Toast.makeText(getBaseContext(),"Message cannot be Empty.",Toast.LENGTH_SHORT);
            t.setGravity(Gravity.TOP|Gravity.CENTER_HORIZONTAL,0,5);
            t.show();
        }
        else
        {
            chatArrayAdapter.add(new ChatMessage(true, chatText.getText().toString()));
            message = chatText.getText().toString();
            chatText.setText("");
            try{
                Toast t = Toast.makeText(getBaseContext(),"Sent",Toast.LENGTH_SHORT);
                t.setGravity(Gravity.TOP|Gravity.CENTER_HORIZONTAL,0,5);
                t.show();
                new Connection().execute();
            }
            catch (Exception e){}
        }
        return true;
    }


    private class Connection extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... params) {

            try {
                URL url = new URL(ip+"/bot/");
                HttpURLConnection connection = (HttpURLConnection)url.openConnection();
                connection.setRequestMethod("POST");
                connection.setRequestProperty("apikey",apikey);
                connection.setRequestProperty("Content-Type","application/json");
                connection.setDoOutput(true);

                JSONObject jsonObject = con.getJson(message);

                DataOutputStream wr = new DataOutputStream(connection.getOutputStream());
                wr.writeBytes(jsonObject.toString());
                wr.flush();
                wr.close();


                InputStream is = connection.getInputStream();

                BufferedReader rd = new BufferedReader(new InputStreamReader(is));

                String line="";
                StringBuffer response = new StringBuffer();
                while((line = rd.readLine()) != null)
                {
                    response.append(line);
                    response.append('\r');
                }
                rd.close();
                //converting reply from server to json object and getting the reply message in reply var
                reply= response.toString();
                JSONObject re = new JSONObject(reply);
                reply = con.getMessage(re).trim();


            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } catch (JSONException e) {
                e.printStackTrace();
            }
            catch (Exception e){}
            return null;
        }

        @Override
        protected void onPostExecute(Void aVoid) {
            super.onPostExecute(aVoid);
            if (reply == "")
            {
                reply = "Bot replied in an alien language.";
            }
            else if (reply.equalsIgnoreCase("You are not Authorized to access this resource"))
            {
                Toast t = Toast.makeText(getBaseContext(),"Access Denied!",Toast.LENGTH_SHORT);
                t.setGravity(Gravity.CENTER_VERTICAL|Gravity.CENTER_HORIZONTAL,0,0);
                t.show();
            }
            chatArrayAdapter.add(new ChatMessage(false, reply));
        }
    }
}