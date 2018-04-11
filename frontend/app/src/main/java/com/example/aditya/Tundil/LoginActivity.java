package com.example.aditya.Tundil;

import android.content.Intent;
import android.content.SharedPreferences;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class LoginActivity extends AppCompatActivity {


    EditText apikey;
    EditText IP;
    String apikeystr;
    private String ip;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        apikey = (EditText)findViewById(R.id.apiEd);
        IP = (EditText)findViewById(R.id.apiIP);

        SharedPreferences prefs = getSharedPreferences("login_data", MODE_PRIVATE);

        if(prefs != null) {
            if (prefs.getBoolean("logged",false))//false is the default value
            {
                apikey.setText(prefs.getString("ApiKey", ""));//null String is the default value
                IP.setText(prefs.getString("IP",""));
                if(apikey.getText().toString().length() != 0)
                    doLogin();
            }
        }

        Button login = (Button)findViewById(R.id.login);
        apikey.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {
            }
            @Override
            public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {
                apikey.setHintTextColor(getResources().getColor(R.color.grey));
                apikey.setHint("API KEY");
            }
            @Override
            public void afterTextChanged(Editable editable) {
            }
        });
        login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                doLogin();
            }
        });

        Button signup = (Button)findViewById(R.id.signup);

        signup.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ip = IP.getText().toString();
                if(ip.length()>0){
                    Bundle b = new Bundle();
                    b.putString("IP",ip);
                    Intent in = new Intent(LoginActivity.this, SignupActivity.class);
                    in.putExtras(b);
                    startActivityForResult(in,1);
                }
                else{
                    invalid_ip();
                }
            }
        });
    }
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 1) {
            if (resultCode == RESULT_OK) {
                String returnString = data.getStringExtra("apikey");
                apikey.setText(returnString);
                doLogin();
            }
        }
    }

    private void invalid_apikey()
    {
        apikey.setText("");
        apikey.setHint("Invalid Api Key");
        apikey.setHintTextColor(getResources().getColor(R.color.red));
        return;
    }
    private void invalid_ip()
    {
        IP.setText("");
        IP.setHint("Invalid IP");
        IP.setHintTextColor(getResources().getColor(R.color.red));
        return;
    }
    private void doLogin()
    {
        apikeystr = apikey.getText().toString();
        ip = IP.getText().toString();
        if(apikeystr.length() == 0 || ip.length() == 0)
        {
            if(apikeystr.length() == 0)
            {
                invalid_apikey();
                apikey.setHint("Required");
            }
            if(ip.length() == 0)
            {
                invalid_ip();
                IP.setHint("Required");
            }

        }
        else if(apikeystr.length() != 0)
        {
            if(apikeystr.length() != 10)
            {
                invalid_apikey();
            }
            else {
                SharedPreferences.Editor editor = getSharedPreferences("login_data", MODE_PRIVATE).edit();
                editor.putBoolean("logged",true);
                editor.putString("ApiKey",apikeystr);
                editor.putString("IP",ip);
                editor.apply();
                Intent in = new Intent(LoginActivity.this,MainActivity.class);
                Bundle bundle = new Bundle();
                bundle.putString("ApiKey",apikeystr);
                bundle.putString("IP",ip);
                in.putExtras(bundle);
                startActivity(in);
            }
        }
    }
}
