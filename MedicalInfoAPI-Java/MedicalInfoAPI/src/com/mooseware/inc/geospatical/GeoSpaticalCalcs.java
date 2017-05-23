package com.mooseware.inc.geospatical;


public class GeoSpaticalCalcs {

	private static double R = 6371e3; // Radius of the Earth in meters
	
	Position getDesinationHaversine(Position from, GeospaticalVector to) throws Exception {
		
		double φ1 = Math.toRadians(from.getLatitude());
		double λ1 = Math.toRadians(from.getLongitude());
		double δ = to.getDistance()/R;
		double brng = Math.toRadians(to.getBearing());
		
		double φ2 = Math.asin( Math.sin(φ1)*Math.cos(δ) + Math.cos(φ1)*Math.sin(δ)*Math.cos(brng) );
		double λ2 = λ1 + Math.atan2(Math.sin(brng)*Math.sin(δ)*Math.cos(φ1), Math.cos(δ)-Math.sin(φ1)*Math.sin(φ2));
		
		return new Position(Math.toDegrees(φ2), Math.toDegrees(λ2));
	}
}
