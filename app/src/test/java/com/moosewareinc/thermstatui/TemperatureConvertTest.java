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
        assertTrue("Room temp is 68F", tc.cToF(20) == 68);
        assertTrue("Boiling is  100C", tc.fToC(212) == 100);
        assertTrue("Frezzing is 0C", tc.fToC(32) == 0);
    }
}
