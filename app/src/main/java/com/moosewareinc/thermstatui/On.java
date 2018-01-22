package com.moosewareinc.thermstatui;

//import android.icu.text.SimpleDateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Calendar;

/**
 * Created by Fred on 3/16/2017.
 */

public class On {
    public Float getTemperature() {
        return temperature;
    }

    public void setTemperature(Float temperature) {
        this.temperature = temperature;
    }

    public String getWhen() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm");
        return sdf.format(when);
        //    return when;
    }

    public void setWhen(String whenStr) throws Exception {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm");
        this.when = sdf.parse(whenStr);
        Date currentTime = Calendar.getInstance().getTime();
        if(when.before(currentTime)) {
            throw new Exception("Warning: Set time: " + whenStr + " is in the past.");
        }
    }

    public String getTemperatureScale() {
        return temperatureScale;
    }

    public void setTemperatureScale(String temperatureScale) {
        this.temperatureScale = temperatureScale;
    }

    private Float temperature;
    private String temperatureScale;
    private Date when;

}