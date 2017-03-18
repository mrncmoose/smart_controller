package com.moosewareinc.thermstatui;

/**
 * Created by Fred on 3/16/2017.
 */

public class On {
    public String getTemperature() {
        return temperature;
    }

    public void setTemperature(String temperature) {
        this.temperature = temperature;
    }

    public String getWhen() {
        return when;
    }

    public void setWhen(String when) {
        this.when = when;
    }

    private String temperature;
    private String when;


}
