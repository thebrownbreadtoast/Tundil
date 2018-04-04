package com.example.aditya.Tundil;

import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
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

public class SignupActivity extends AppCompatActivity {

    private EditText name;
    private EditText phn;
    private TextView errorbox;
    private String phnstr;
    private String namestr;

    private Convert con = new Convert();
    private JSONObject jsonObject;

    private String reply="";

    private String ip="";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);
        name = (EditText)findViewById(R.id.nameEd);
        phn = (EditText)findViewById(R.id.phnsEd);
        errorbox = (TextView)findViewById(R.id.erorbox);
        Bundle bundle = getIntent().getExtras();
        ip = bundle.getString("IP");

        Button register = (Button)findViewById(R.id.register);
        register.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                errorbox.setText("");
                reply ="";
                phnstr = phn.getText().toString();
                namestr = name.getText().toString();
                doRegistration();
            }
        });

    }

    private void invalid_phn()
    {
        phn.setText("");
        phn.setHint("Invalid Phone Number");
        phn.setHintTextColor(getResources().getColor(R.color.red));
        errorbox.setText("Check Details!");
        return;
    }
    private void invalid_name()
    {
        name.setText("");
        name.setHint("Invalid Phone Number");
        name.setHintTextColor(getResources().getColor(R.color.red));
        errorbox.setText("Check Details!");
        return;
    }
    private void doRegistration()
    {
        if(phnstr.length() == 0 || namestr.length() == 0)
        {
            if(phnstr.length() == 0)
            {
                invalid_phn();
                phn.setHint("Required");
            }
            if(namestr.length() == 0)
            {
                invalid_name();
                name.setHint("Required");
            }
            return;
        }

        if((phnstr.length() != 0) && (namestr.length() != 0))
        {
            if(phnstr.length() != 10)
            {
                invalid_phn();
                return;
            }
        }
        try {jsonObject = con.getSignupJson(namestr,Integer.parseInt(phnstr));}catch (Exception e){}
        new Connection().execute();
    }
    private class Connection extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... params) {

            try {
                URL url = new URL(ip+":5000/bot/register");
                HttpURLConnection connection = (HttpURLConnection)url.openConnection();
                connection.setRequestMethod("POST");
                connection.setRequestProperty("Content-Type","application/json");
                connection.setDoOutput(true);
                DataOutputStream wr = new DataOutputStream(connection.getOutputStream());
                wr.writeBytes("{\"name\":\""+namestr+"\",\"phone\":"+phnstr+"}");
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


            if (reply.equalsIgnoreCase("You are not Authorized to access this resource"))
            {
                Toast.makeText(getBaseContext(),"Access Denied",Toast.LENGTH_LONG).show();
            }
            if(reply.equalsIgnoreCase("Something went wrong."))
            {
                Toast.makeText(getBaseContext(),reply,Toast.LENGTH_LONG).show();
                errorbox.setText("Please try again.");
            }
            else{
                Intent returnIntent = getIntent();
                returnIntent.putExtra("apikey",reply);
                setResult(RESULT_OK,returnIntent);
                finish();
            }
        }
    }
}
