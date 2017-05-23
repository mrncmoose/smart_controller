package com.mooseware.inc.geospatical;

import static org.junit.Assert.*;

import org.junit.Test;

public class GeoSpaticalCalcsTest {

	@Test
	public void testGetDesinationHaversine() {
		GeoSpaticalCalcs gsc = new GeoSpaticalCalcs();
		try {
			GeospaticalVector offset = new GeospaticalVector(14.60d, 130.27d);
			Position p = new Position(44.93305739304405d, -74.38450407239078d);
			Position p2 = gsc.getDesinationHaversine(p, offset);
			System.out.println("Offset position: " + p2.getLatitude() + " " + p2.getLongitude());
			assertEquals("Latitude is incorrect", p2.getLatitude(), 44.93297293696693d, 0.00003);
			assertEquals("Longitude is incorrect", p2.getLongitude(), -74.38436214157258d, 0.00003);
		} catch (Exception e) {
			e.printStackTrace();
			fail("Bad geosptical vector");
		}
		
		assertTrue("Pass", true);
	}

}
