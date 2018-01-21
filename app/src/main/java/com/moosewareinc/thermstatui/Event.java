package com.moosewareinc.thermstatui;

/**
 * Created by Fred on 3/16/2017.
 */

//Defines the datatype for the thermal event to send to the thermal controller.
public class Event {
    private On on;
    private Off off;

    public On getOn() {
        return on;
    }

    public void setOn(On on) throws Exception {
        this.on = on;
    }

    public Off getOff() {
        return off;
    }

    public void setOff(Off off) throws Exception{
        this.off = off;
    }


}
