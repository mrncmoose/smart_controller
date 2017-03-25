package com.moosewareinc.thermstatui;

import android.app.DatePickerDialog;
import android.app.TimePickerDialog;
import android.content.DialogInterface;
import android.os.CountDownTimer;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
//import android.widget.DatePicker;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.TextView;
import android.widget.TimePicker;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.Calendar;
import java.util.HashMap;
import java.util.Map;
import java.util.Timer;
import java.util.TimerTask;

public class SettingsActivity extends AppCompatActivity implements View.OnClickListener {

    private static final String url = "http://192.168.42.1:5000";
    private static final String currentTempResource = "/thermal/api/v1.0/current_temp";
    private static final String eventsResource = "/thermal/api/v1.0/events";
    private TextView onTempText;
    private TextView onDateText;
    private TextView onTimeText;
    private TextView offTempText;
    private TextView offDateText;
    private TextView offTimeText;
    private TextView currentTempText;
    private Button setOnDateButton;
    private Button setOnTimeButton;
    private Button setOffDateButton;
    private Button setOffTimeButton;
    private int mYear, mMonth, mDay, mHour, mMinute;
    private Timer getTempTimer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);
        //TODO:  get current values & populate
        onTempText = (TextView) findViewById(R.id.onTempText);
        onDateText = (TextView) findViewById(R.id.onDateText);
        onTimeText = (TextView) findViewById(R.id.onTimeText);
        offTempText = (TextView) findViewById(R.id.offTempText);
        offDateText = (TextView) findViewById(R.id.offDateText);
        offTimeText = (TextView) findViewById(R.id.offTimeText);
        currentTempText = (TextView) findViewById(R.id.currentTempText);
        setOnDateButton = (Button) findViewById(R.id.setOnDateButton);
        setOnTimeButton = (Button) findViewById(R.id.setOnTimeButton);
        setOffDateButton = (Button) findViewById(R.id.setOffDateButton);
        setOffTimeButton = (Button) findViewById(R.id.setOffTimeButton);

        setOnDateButton.setOnClickListener(this);
        setOnTimeButton.setOnClickListener(this);
        setOffDateButton.setOnClickListener(this);
        setOffTimeButton.setOnClickListener(this);

        getTempTimer = new Timer();
        TimerTask t = new TimerTask() {

            @Override
            public void run() {
                loadCurrentTemp();
            }
        };
        getTempTimer.scheduleAtFixedRate(t, 2000, 10000);
        loadCurrentTemp();
        loadCurrentEvent();
    }

    private void loadCurrentTemp() {
        JsonObjectRequest jsObjRequest = new JsonObjectRequest
                (Request.Method.GET, url+currentTempResource, null, new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            String temp = "Current temp: " + response.getString("current_temp") + "C";
                            currentTempText.setText(temp);
                        } catch(Exception e) {
                            AlertDialog ad = new AlertDialog.Builder(SettingsActivity.this).create();
                            ad.setTitle("Error getting current temperature");
                            ad.setMessage("Error getting current temperature: " + e.getMessage());
                            ad.setButton(AlertDialog.BUTTON_NEUTRAL, "Ok",
                                    new DialogInterface.OnClickListener() {
                                        public void onClick(DialogInterface dialog, int which) {
                                            dialog.dismiss();
                                        }
                                    });
                            ad.show();
                        }
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        String errMsg = "Error getting current temp: " + error.toString();
                        AlertDialog ad = new AlertDialog.Builder(SettingsActivity.this).create();
                        ad.setTitle("Error getting current temperature");
                        ad.setMessage(errMsg);
                        ad.setButton(AlertDialog.BUTTON_NEUTRAL, "Ok",
                                new DialogInterface.OnClickListener() {
                                    public void onClick(DialogInterface dialog, int which) {
                                        dialog.dismiss();
                                    }
                                });
                        ad.show();
                    }
                });
        RequestQueSingleton.getmInstance(this).addToRequestQueue(jsObjRequest);
    }

    private void loadCurrentEvent() {
        JsonObjectRequest jsObjRequest = new JsonObjectRequest
                (Request.Method.GET, url+eventsResource, null, new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            JSONArray events = response.getJSONArray("events");
                            JSONObject jevent = (JSONObject) events.get(0);
                            JSONObject onObj = jevent.getJSONObject("on");
                            String onTemp = onObj.getString("temperature");
                            String onDateTime[] = parseDateTime(onObj.getString("when"));
                            onDateText.setText(onDateTime[0]);
                            onTimeText.setText(onDateTime[1]);
                            onTempText.setText(onTemp);
                            JSONObject offObj = jevent.getJSONObject("off");
                            String offTemp = offObj.getString("temperature");
                            String offDateTime[] = parseDateTime(offObj.getString("when"));
                            offDateText.setText(offDateTime[0]);
                            offTimeText.setText(offDateTime[1]);
                            offTempText.setText(offTemp);
                        } catch(Exception e) {
                            AlertDialog ad = new AlertDialog.Builder(SettingsActivity.this).create();
                            ad.setTitle("Error getting thermal events");
                            ad.setMessage("Error getting event array: " + e.getMessage());
                            ad.setButton(AlertDialog.BUTTON_NEUTRAL, "Ok",
                                    new DialogInterface.OnClickListener() {
                                        public void onClick(DialogInterface dialog, int which) {
                                            dialog.dismiss();
                                        }
                                    });
                            ad.show();
                        }
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        String errMsg = "Error getting thermal events: " + error.toString();
                        AlertDialog ad = new AlertDialog.Builder(SettingsActivity.this).create();
                        ad.setTitle("Error getting thermal events");
                        ad.setMessage(errMsg);
                        ad.setButton(AlertDialog.BUTTON_NEUTRAL, "Ok",
                                new DialogInterface.OnClickListener() {
                                    public void onClick(DialogInterface dialog, int which) {
                                        dialog.dismiss();
                                    }
                                });
                        ad.show();
                    }
                });
        RequestQueSingleton.getmInstance(this).addToRequestQueue(jsObjRequest);
    }

    public void setEvent(View view) {
        // assemble and send the event JSON message to the controller
        String offDateTime = offDateText.getText().toString() + " " + offTimeText.getText().toString();
        String onDateTime = onDateText.getText().toString() + " " + onTimeText.getText().toString();
        try {
            JSONArray jArray = new JSONArray();
            JSONObject jObj = new JSONObject();
            JSONObject onObj = new JSONObject();
            onObj.put("when", onDateTime);
            onObj.put("temperature", onTempText.getText().toString());
            JSONObject offObj = new JSONObject();
            offObj.put("when", offDateTime);
            offObj.put("temperature", offTempText.getText().toString());
            JSONObject events = new JSONObject();
            events.put("on", onObj);
            events.put("off", offObj);
            jArray.put(events);
            jObj.put("events", jArray);
        JsonObjectRequest jsonObjRequest = new JsonObjectRequest
                (Request.Method.POST, url + eventsResource, jObj, new Response.Listener<JSONObject>()
                {
                    @Override
                    public void onResponse(JSONObject response)
                    {
                        Toast.makeText(getApplicationContext(), "Successfully sent thermal events", Toast.LENGTH_LONG).show();
                    }
                },
                        new Response.ErrorListener()
                        {
                            @Override
                            public void onErrorResponse(VolleyError error)
                            {
                                //Toast.makeText(getApplicationContext(), error.toString(), Toast.LENGTH_LONG).show();
                                AlertDialog ad = new AlertDialog.Builder(SettingsActivity.this).create();
                                ad.setTitle("Error saving thermal events");
                                ad.setMessage(error.toString());
                                ad.setButton(AlertDialog.BUTTON_NEUTRAL, "Ok",
                                        new DialogInterface.OnClickListener() {
                                            public void onClick(DialogInterface dialog, int which) {
                                                dialog.dismiss();
                                            }
                                        });
                                ad.show();

                            }
                        });
        RequestQueSingleton.getmInstance(this).addToRequestQueue(jsonObjRequest);
        } catch (JSONException e) {
            Toast.makeText(getApplicationContext(), e.getMessage(), Toast.LENGTH_LONG).show();
        }
    }

    //WARNING:  This method does not handle badly formed date time strings!
    // safe for the moment because there is good control over the date time string.
    // Note:  the only reason for doing this is backward compatiblilty to android 5.
    //TODO:  add throws exception
    // returns date + time
    public String[] parseDateTime(String dt) {
        String dateTime[] = dt.split(" ");
        return  dateTime;
    }

    @Override
    public void onClick(View v) {
        final Calendar c = Calendar.getInstance();
        if(v ==setOnDateButton) {
            mYear = c.get(Calendar.YEAR);
            mMonth = c.get(Calendar.MONTH);
            mDay = c.get(Calendar.DAY_OF_MONTH);
            DatePickerDialog datePickerDialog = new DatePickerDialog(this, new DatePickerDialog.OnDateSetListener() {
                @Override
                public void onDateSet(DatePicker view, int year, int monthOfYear, int dayOfMonth)
                {
                    String dateStr = String.format("%d-%02d-%02d", year, monthOfYear+1, dayOfMonth);
                    onDateText.setText(dateStr);
                }
            }, mYear, mMonth, mDay);
            datePickerDialog.show();
        }

        if(v ==setOnTimeButton) {
            mHour = c.get(Calendar.HOUR_OF_DAY);
            mMinute = c.get(Calendar.MINUTE);
            TimePickerDialog timePickerDialog = new TimePickerDialog(this,
                    new TimePickerDialog.OnTimeSetListener() {
                        @Override
                        public void onTimeSet(TimePicker view, int hourOfDay,
                                              int minute)
                        {
                            String timeStr = String.format("%02d:%02d", hourOfDay, minute);
                            onTimeText.setText(timeStr);
                        }
                    }, mHour, mMinute, false);
            timePickerDialog.show();
        }

        if(v==setOffDateButton) {
            mYear = c.get(Calendar.YEAR);
            mMonth = c.get(Calendar.MONTH);
            mDay = c.get(Calendar.DAY_OF_MONTH);
            DatePickerDialog datePickerDialog = new DatePickerDialog(this, new DatePickerDialog.OnDateSetListener() {
                @Override
                public void onDateSet(DatePicker view, int year, int monthOfYear, int dayOfMonth)
                {
                    String dateStr = String.format("%d-%02d-%02d", year, monthOfYear+1, dayOfMonth);
                    offDateText.setText(dateStr);
                }
            }, mYear, mMonth, mDay);
            datePickerDialog.show();
        }

        if(v==setOffTimeButton) {
            mHour = c.get(Calendar.HOUR_OF_DAY);
            mMinute = c.get(Calendar.MINUTE);
            TimePickerDialog timePickerDialog = new TimePickerDialog(this,
                    new TimePickerDialog.OnTimeSetListener() {
                        @Override
                        public void onTimeSet(TimePicker view, int hourOfDay,
                                              int minute)
                        {
                            String timeStr = String.format("%02d:%02d", hourOfDay, minute);
                            offTimeText.setText(timeStr);
                        }
                    }, mHour, mMinute, false);
            timePickerDialog.show();
        }
    }
}