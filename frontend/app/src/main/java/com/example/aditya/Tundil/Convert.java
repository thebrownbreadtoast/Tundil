package com.example.aditya.Tundil;

/**
 * Created by ADITYA on 23 Mar 2018.
 */
        import org.json.JSONException;
        import org.json.JSONObject;

public class Convert {
    JSONObject jsonObject;

    public JSONObject getJson(String value) throws JSONException {
        jsonObject = new JSONObject();
        jsonObject.put("reply", value);
        return jsonObject;
    }
    public JSONObject getSignupJson(String name, int num) throws JSONException {
        jsonObject = new JSONObject();
        jsonObject.put("name", name);
        jsonObject.put("phone", num);
        return jsonObject;
    }

    public String getMessage(JSONObject obj) throws JSONException{
        String str = obj.getString("reply");
        return  str;
    }
}