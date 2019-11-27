package com.moosewareinc.thermstatui;

/**
 * Created by Fred on 3/19/2017.
 */

public class TemperatureConvert {

    public float cToF(float c) {
        return c * 1.8f +32f;
    }

    public float fToC(float f) {
        return (f - 32)/1.8f;
    }
}
