package com.moosewareinc.thermstatui;

import org.junit.Test;

import static org.junit.Assert.*;

/**
 * Created by Fred on 3/19/2017.
 */

public class TemperatureConvertTest {
    @Test
    public void cToF() {
        TemperatureConvert tc = new TemperatureConvert();
        float RoomTemp = tc.cToF(20.0f);
        System.out.println("Room temp in F: " + RoomTemp);
        float bpC = tc.fToC(212.0f);
        System.out.println("Boiling piont in C: " + bpC);
        assertTrue("Room temp is 68F", tc.cToF(20f) == 68);
        assertTrue("Boiling is  100C", tc.fToC(212f) == 100);
        assertTrue("Frezzing is 0C", tc.fToC(32f) == 0);
    }
}
